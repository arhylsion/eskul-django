import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eskul_project.settings')
django.setup()

from accounts.models import Student
from eskul.models import Extracurricular, Registration
from quiz.models import Question, QuizResult
from django.contrib.auth.models import User
import random

def seed():
    print("Clearing existing data...")
    QuizResult.objects.all().delete()
    Registration.objects.all().delete()
    Question.objects.all().delete()
    Student.objects.all().delete()
    Extracurricular.objects.all().delete()
    User.objects.filter(is_superuser=True).delete()

    print("Seeding fresh data...")

    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin created (user: admin, pass: admin123)")

    eskuls = ['Pramuka', 'PMR', 'Basket', 'Futsal', 'Paduan Suara', 'KIR', 'Rohis', 'Robotik', 'Jurnalistik']
    for e in eskuls:
        Extracurricular.objects.create(nama_eskul=e)
    print("Extracurriculars created.")

    questions_data = [
        {'soal': 'Apa manfaat mengikuti ekstrakurikuler?', 'a': 'Beban tugas', 'b': 'Kurang main', 'c': 'Soft skill', 'd': 'Nilai gratis', 'ans': 'C', 'pt': 20},
        {'soal': 'Cara pilih eskul?', 'a': 'Populer', 'b': 'Ikut teman', 'c': 'Minat bakat', 'd': 'Acak', 'ans': 'C', 'pt': 20},
        {'soal': 'Eskul bantu prestasi?', 'a': 'Tidak', 'b': 'Ya, manajemen waktu', 'c': 'Biasa saja', 'd': 'Hanya paksaan', 'ans': 'B', 'pt': 20},
        {'soal': 'Contoh eskul populer?', 'a': 'Pramuka/PMR', 'b': 'Game online', 'c': 'Nonton TV', 'd': 'Tidur', 'ans': 'A', 'pt': 20},
        {'soal': 'Bagi waktu sekolah-eskul?', 'a': 'Begadang', 'b': 'Jadwal teratur', 'c': 'Bolos kelas', 'd': 'Pas ujian saja', 'ans': 'B', 'pt': 20}
    ]
    for q in questions_data:
        Question.objects.create(soal=q['soal'], pilihan_a=q['a'], pilihan_b=q['b'], pilihan_c=q['c'], pilihan_d=q['d'], jawaban_benar=q['ans'], point=q['pt'])
    print("Questions created.")

    first_names = ["Budi", "Siti", "Joko", "Rina", "Agung", "Dewi", "Ahmad", "Maya", "Reza", "Tara", "Nicho", "Putri", "Rizky", "Ayu", "Doni", "Bagas", "Cindy", "Irfan", "Melisa", "Galih"]
    last_names = ["Santoso", "Aminah", "Anwar", "Nose", "Hercules", "Lestari", "Dhani", "Septha", "Rahadian", "Basro", "Saputra", "Maharani", "Pratama", "Safitri", "Setiawan", "Firmansyah", "Rahayu", "Hakim", "Andriani", "Pramudya"]

    eskul_list = list(Extracurricular.objects.all())
    
    print("Generating 49 students...")
    for i in range(49):
        nis = f"2425{i:03d}"
        nama = f"{random.choice(first_names)} {random.choice(last_names)}"
        kelas = f"{random.choice([10, 11, 12])} {random.choice(['A', 'B', 'C', 'D'])}"
        
        student = Student.objects.create(
            nis=nis,
            password='password123',
            nama=nama,
            kelas=kelas
        )

        if i < 15:
            chosen_eskul = random.choice(eskul_list)
            status = random.choice(['pending', 'approved', 'rejected'])
            
            Registration.objects.create(
                student=student,
                eskul=chosen_eskul,
                status=status,
                notes=f"Saya berminat masuk {chosen_eskul.nama_eskul}."
            )
            
            score = random.randint(4, 10) * 10
            QuizResult.objects.create(student=student, score=score)
            
            if status == 'approved':
                student.has_eskul = True
                student.save()

    print("Successfully seeded 50 accounts (1 Admin, 49 Students).")
    print("15 students have registrations with random status.")

if __name__ == '__main__':
    seed()
