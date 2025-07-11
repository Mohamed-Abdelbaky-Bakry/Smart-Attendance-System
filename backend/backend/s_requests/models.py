import email
from pickle import TRUE
from queue import Empty
from django.utils import timezone
from django.db import models
from users.models import GRADE_CHOICES, Student
from academics.models import Subject

class Request(models.Model):
    REQUEST_TYPES = [
        ('absence', 'Absence Excuse'),
        ('late', 'Late Justification'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    instructor_comment = models.CharField(max_length=255, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.account.name} - {self.request_type} - {self.status}"
