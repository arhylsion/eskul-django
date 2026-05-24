import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eskul_project.settings')
django.setup()

from accounts.models import Student
from eskul.models import Extracurricular, Registration
from quiz.models import Question, QuizResult
from django.contrib.auth.models import User


def seed():
    print("Clearing existing data...")

    QuizResult.objects.all().delete()
    Registration.objects.all().delete()
    Question.objects.all().delete()
    Student.objects.all().delete()
    Extracurricular.objects.all().delete()
    User.objects.filter(is_superuser=True).delete()

    print("Seeding fresh data...")

    User.objects.create_superuser(
        'admin',
        'admin@example.com',
        'admin123'
    )

    print("Admin created.")

    eskuls = [
        'Pramuka',
        'PMR',
        'Basket',
        'Futsal',
        'Paduan Suara',
        'KIR',
        'Rohis',
        'Robotik',
        'Jurnalistik'
    ]

    for e in eskuls:
        Extracurricular.objects.create(
            nama_eskul=e
        )

    print("Extracurriculars created.")

    questions_data = [
        {
            'soal': 'Apa manfaat mengikuti ekstrakurikuler?',
            'a': 'Beban tugas',
            'b': 'Kurang main',
            'c': 'Soft skill',
            'd': 'Nilai gratis',
            'ans': 'C',
            'pt': 20
        },
        {
            'soal': 'Cara pilih eskul?',
            'a': 'Populer',
            'b': 'Ikut teman',
            'c': 'Minat bakat',
            'd': 'Acak',
            'ans': 'C',
            'pt': 20
        },
        {
            'soal': 'Eskul bantu prestasi?',
            'a': 'Tidak',
            'b': 'Ya, manajemen waktu',
            'c': 'Biasa saja',
            'd': 'Hanya paksaan',
            'ans': 'B',
            'pt': 20
        },
        {
            'soal': 'Contoh eskul populer?',
            'a': 'Pramuka/PMR',
            'b': 'Game online',
            'c': 'Nonton TV',
            'd': 'Tidur',
            'ans': 'A',
            'pt': 20
        },
        {
            'soal': 'Bagi waktu sekolah-eskul?',
            'a': 'Begadang',
            'b': 'Jadwal teratur',
            'c': 'Bolos kelas',
            'd': 'Pas ujian saja',
            'ans': 'B',
            'pt': 20
        }
    ]

    for q in questions_data:
        Question.objects.create(
            soal=q['soal'],
            pilihan_a=q['a'],
            pilihan_b=q['b'],
            pilihan_c=q['c'],
            pilihan_d=q['d'],
            jawaban_benar=q['ans'],
            point=q['pt']
        )

    print("Questions created.")

    first_names = [
        "Budi","Siti","Joko","Rina","Agung",
        "Dewi","Ahmad","Maya","Reza","Tara",
        "Nicho","Putri","Rizky","Ayu","Doni",
        "Bagas","Cindy","Irfan","Melisa","Galih"
    ]

    last_names = [
        "Santoso","Aminah","Anwar","Nose",
        "Hercules","Lestari","Dhani","Septha",
        "Rahadian","Basro","Saputra","Maharani",
        "Pratama","Safitri","Setiawan",
        "Firmansyah","Rahayu","Hakim",
        "Andriani","Pramudya"
    ]

    eskul_list = list(
        Extracurricular.objects.all()
    )

    print("Generating students...")

    for i in range(49):

        student = Student.objects.create(
            nis=f"2425{i:03d}",
            password="password123",
            nama=f"{random.choice(first_names)} {random.choice(last_names)}",
            kelas=f"{random.choice([10,11,12])} {random.choice(['A','B','C','D'])}"
        )

        if i < 15:

            chosen_eskul = random.choice(
                eskul_list
            )

            if i < 5:

                score = random.choice(
                    [70, 80, 90, 100]
                )

                status = "approved"

                student.has_eskul = True
                student.save()

                approved_at = timezone.now()

                can_retry = False

            elif i < 10:

                score = random.choice(
                    [70, 80, 90]
                )

                status = "pending"

                approved_at = None

                can_retry = False

            else:

                score = random.choice(
                    [40, 50, 60]
                )

                status = "rejected"

                approved_at = None

                can_retry = True

            Registration.objects.create(
                student=student,
                eskul=chosen_eskul,
                status=status,
                approved_at=approved_at,
                notes=f"Saya berminat masuk {chosen_eskul.nama_eskul}."
            )

            QuizResult.objects.create(
                student=student,
                score=score,
                can_retry=can_retry
            )

    print("Done.")
    print("49 students generated.")
    print("5 approved, 5 pending, 5 rejected(retry enabled).")


if __name__ == "__main__":
    seed()