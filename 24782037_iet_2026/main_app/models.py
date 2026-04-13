from django.core.exceptions import ValidationError
from django.db import models

STATUS_CHOICES = [
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

class Report(models.Model):
    reporter_name = models.CharField(max_length=100)  # 🔥 TAMBAHAN (nama pelapor)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        valid_statuses = [choice[0] for choice in STATUS_CHOICES]
        if self.status not in valid_statuses:
            raise ValidationError({'status': 'Status tidak valid.'})


class ReportStatusChange(models.Model):
    report = models.ForeignKey(Report, related_name='status_changes', on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.report.title}: {self.get_old_status_display()} → {self.get_new_status_display()}"