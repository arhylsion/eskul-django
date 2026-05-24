from django.db import models
from accounts.models import Student

class QuizResult(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(default=0)

    can_retry = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.student.nama

class Question(models.Model):

    soal = models.TextField()

    pilihan_a = models.CharField(max_length=255)
    pilihan_b = models.CharField(max_length=255)
    pilihan_c = models.CharField(max_length=255)
    pilihan_d = models.CharField(max_length=255)

    jawaban_benar = models.CharField(max_length=1)

    point = models.IntegerField(default=10)

    def __str__(self):
        return self.soal

    def get_options(self):
        return {
            'A': self.pilihan_a,
            'B': self.pilihan_b,
            'C': self.pilihan_c,
            'D': self.pilihan_d,
        }
