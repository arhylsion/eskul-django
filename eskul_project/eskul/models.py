from django.db import models
from accounts.models import Student

class Extracurricular(models.Model):

    nama_eskul = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_eskul

class Registration(models.Model):

    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    eskul = models.ForeignKey(
        Extracurricular,
        on_delete=models.CASCADE
    )

    notes = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.student.nama
