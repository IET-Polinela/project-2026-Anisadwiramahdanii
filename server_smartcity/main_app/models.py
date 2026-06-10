from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

STATUS_TRANSITIONS = {
    'DRAFT': 'REPORTED',
    'REPORTED': 'VERIFIED',
    'VERIFIED': 'IN_PROGRESS',
    'IN_PROGRESS': 'RESOLVED',
    'RESOLVED': None,
}

STATUS_BADGE_CLASSES = {
    'DRAFT': 'text-bg-secondary',
    'REPORTED': 'text-bg-warning',
    'VERIFIED': 'text-bg-info',
    'IN_PROGRESS': 'text-bg-primary',
    'RESOLVED': 'text-bg-success',
}


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reports',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reporter_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})

    def clean(self):
        valid_statuses = [choice[0] for choice in STATUS_CHOICES]
        if self.status not in valid_statuses:
            raise ValidationError({'status': 'Status tidak valid.'})

    @property
    def status_badge_class(self):
        return STATUS_BADGE_CLASSES.get(self.status, 'text-bg-secondary')

    @property
    def next_status(self):
        next_status_code = STATUS_TRANSITIONS.get(self.status)
        if not next_status_code:
            return None

        status_map = dict(STATUS_CHOICES)
        return {
            'value': next_status_code,
            'label': status_map[next_status_code],
        }


class ReportStatusChange(models.Model):
    report = models.ForeignKey(Report, related_name='status_changes', on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.report.title}: {self.get_old_status_display()} -> {self.get_new_status_display()}"

    @property
    def new_status_badge_class(self):
        return STATUS_BADGE_CLASSES.get(self.new_status, 'text-bg-secondary')
