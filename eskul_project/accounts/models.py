from django.db import models

class Student(models.Model):

    nis = models.CharField(max_length=20, unique=True)

    password = models.CharField(max_length=100)

    nama = models.CharField(max_length=100)

    kelas = models.CharField(max_length=20)

    has_eskul = models.BooleanField(default=False)

    def __str__(self):
        return self.nama
