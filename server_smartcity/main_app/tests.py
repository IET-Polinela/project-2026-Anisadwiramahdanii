from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Report


class ReportJWTAPITests(APITestCase):
    password = '12345678'

    def test_web_login_accepts_admin_and_citizen_accounts(self):
        admin = get_user_model().objects.create_superuser(
            username='admin',
            password=self.password,
            email='admin@example.com',
        )
        citizen = get_user_model().objects.create_user(
            username='anisa',
            password=self.password,
            email='anisa@example.com',
            is_admin=False,
            is_member=True,
        )

        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_member)

        for username in [admin.username, citizen.username]:
            response = self.client.post(
                '/accounts/login/',
                {
                    'username': username,
                    'password': self.password,
                },
            )

            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.url, '/')
            self.client.logout()

    def test_citizen_can_register_login_and_create_anonymous_draft_report(self):
        register_response = self.client.post(
            '/api/register/',
            {
                'username': 'anisa',
                'email': 'anisa@example.com',
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        token_response = self.client.post(
            '/api/token/',
            {
                'username': 'anisa',
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        create_response = self.client.post(
            '/api/reports/',
            {
                'title': 'Jalan berlubang',
                'category': 'Infrastruktur',
                'description': 'Ada lubang besar di dekat halte.',
                'location': 'Jl. Merdeka',
            },
            format='json',
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get()
        self.assertEqual(report.reporter.username, 'anisa')
        self.assertEqual(report.reporter_name, 'Warga Anonim')
        self.assertEqual(report.status, 'DRAFT')

        list_response = self.client.get('/api/reports/')

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data['results']), 1)
        self.assertEqual(list_response.data['results'][0]['reporter'], 'Warga Anonim')
        self.assertTrue(list_response.data['results'][0]['is_owner'])

    def test_owner_cannot_delete_verified_report(self):
        user = get_user_model().objects.create_user(
            username='citizen11',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        report = Report.objects.create(
            reporter=user,
            reporter_name='Warga Anonim',
            title='Lampu rusak',
            category='Fasilitas',
            description='Lampu jalan mati.',
            location='Jl. Sudirman',
            status='VERIFIED',
        )

        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/reports/{report.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Report.objects.filter(id=report.id).exists())

    def test_list_and_detail_follow_lab_visibility_flow(self):
        admin = get_user_model().objects.create_superuser(
            username='admin',
            password=self.password,
            email='admin@example.com',
        )
        citizen1 = get_user_model().objects.create_user(
            username='anisa',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        citizen2 = get_user_model().objects.create_user(
            username='budi',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        verified_report = Report.objects.create(
            reporter=admin,
            reporter_name='Admin',
            title='Laporan terverifikasi',
            category='Umum',
            description='Laporan yang sudah terlihat publik.',
            location='Kantor',
            status='VERIFIED',
        )
        report1 = Report.objects.create(
            reporter=citizen1,
            reporter_name='Warga Anonim',
            title='Report1',
            category='Infrastruktur',
            description='Draft milik citizen1.',
            location='Lokasi 1',
            status='DRAFT',
        )
        report2 = Report.objects.create(
            reporter=citizen2,
            reporter_name='Warga Anonim',
            title='Report2',
            category='Fasilitas',
            description='Draft milik citizen2.',
            location='Lokasi 2',
            status='DRAFT',
        )

        self.client.force_authenticate(user=admin)
        admin_response = self.client.get('/api/reports/')
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {report['id'] for report in admin_response.data['results']},
            {verified_report.id},
        )
        self.assertEqual(
            self.client.get(f'/api/reports/{report1.id}/').status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.client.force_authenticate(user=citizen1)
        citizen1_response = self.client.get('/api/reports/')
        self.assertEqual(citizen1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {report['id'] for report in citizen1_response.data['results']},
            {verified_report.id, report1.id},
        )
        self.assertEqual(
            self.client.get(f'/api/reports/{report1.id}/').status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.get(f'/api/reports/{report2.id}/').status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.client.force_authenticate(user=citizen2)
        citizen2_response = self.client.get('/api/reports/')
        self.assertEqual(citizen2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {report['id'] for report in citizen2_response.data['results']},
            {verified_report.id, report2.id},
        )

    def test_lab12_tab_filtering_pagination_and_submission_flow(self):
        citizen1 = get_user_model().objects.create_user(
            username='anisa',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        citizen2 = get_user_model().objects.create_user(
            username='budi',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        own_draft = Report.objects.create(
            reporter=citizen1,
            reporter_name='Warga Anonim',
            title='Draft saya',
            category='Infrastruktur',
            description='Masih draft.',
            location='Lokasi 1',
            status='DRAFT',
        )
        own_reported = Report.objects.create(
            reporter=citizen1,
            reporter_name='Warga Anonim',
            title='Laporan saya',
            category='Umum',
            description='Sudah diajukan.',
            location='Lokasi 2',
            status='REPORTED',
        )
        other_reported = Report.objects.create(
            reporter=citizen2,
            reporter_name='Warga Anonim',
            title='Laporan warga lain',
            category='Fasilitas',
            description='Terlihat di feed.',
            location='Lokasi 3',
            status='REPORTED',
        )
        Report.objects.create(
            reporter=citizen2,
            reporter_name='Warga Anonim',
            title='Draft warga lain',
            category='Fasilitas',
            description='Tidak boleh masuk feed.',
            location='Lokasi 4',
            status='DRAFT',
        )

        self.client.force_authenticate(user=citizen1)

        my_reports = self.client.get('/api/reports/?tab=my_reports')
        self.assertEqual(my_reports.status_code, status.HTTP_200_OK)
        self.assertEqual(my_reports.data['count'], 2)
        self.assertEqual(
            {report['id'] for report in my_reports.data['results']},
            {own_draft.id, own_reported.id},
        )

        feed = self.client.get('/api/reports/?tab=feed')
        self.assertEqual(feed.status_code, status.HTTP_200_OK)
        self.assertEqual(feed.data['count'], 1)
        self.assertEqual(feed.data['results'][0]['id'], other_reported.id)
        self.assertEqual(feed.data['results'][0]['reporter'], 'Warga Anonim')
        self.assertFalse(feed.data['results'][0]['is_owner'])

        submit_response = self.client.put(
            f'/api/reports/{own_draft.id}/',
            {
                'title': own_draft.title,
                'category': own_draft.category,
                'description': own_draft.description,
                'location': own_draft.location,
                'status': 'REPORTED',
            },
            format='json',
        )
        self.assertEqual(submit_response.status_code, status.HTTP_200_OK)
        own_draft.refresh_from_db()
        self.assertEqual(own_draft.status, 'REPORTED')

    def test_admin_only_changes_status_and_citizen_manages_own_draft(self):
        admin = get_user_model().objects.create_superuser(
            username='admin',
            password=self.password,
            email='admin@example.com',
        )
        citizen1 = get_user_model().objects.create_user(
            username='anisa',
            password=self.password,
            is_admin=False,
            is_member=True,
        )
        report = Report.objects.create(
            reporter=citizen1,
            reporter_name='Warga Anonim',
            title='Report1',
            category='Infrastruktur',
            description='Draft milik citizen1.',
            location='Lokasi 1',
            status='DRAFT',
        )
        verified_report = Report.objects.create(
            reporter=citizen1,
            reporter_name='Warga Anonim',
            title='Report publik',
            category='Umum',
            description='Laporan sudah verified.',
            location='Lokasi publik',
            status='VERIFIED',
        )

        self.client.force_authenticate(user=admin)
        admin_status_response = self.client.patch(
            f'/api/reports/{verified_report.id}/',
            {'status': 'IN_PROGRESS'},
            format='json',
        )
        self.assertEqual(admin_status_response.status_code, status.HTTP_200_OK)
        verified_report.refresh_from_db()
        self.assertEqual(verified_report.status, 'IN_PROGRESS')

        admin_edit_response = self.client.patch(
            f'/api/reports/{verified_report.id}/',
            {'title': 'Diubah admin'},
            format='json',
        )
        self.assertEqual(admin_edit_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=citizen1)
        citizen_edit_response = self.client.patch(
            f'/api/reports/{report.id}/',
            {'title': 'Report1 diperbarui'},
            format='json',
        )
        self.assertEqual(citizen_edit_response.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        self.assertEqual(report.title, 'Report1 diperbarui')

        citizen_delete_response = self.client.delete(f'/api/reports/{report.id}/')
        self.assertEqual(citizen_delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Report.objects.filter(id=report.id).exists())
