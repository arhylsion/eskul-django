# Eskul Project

Project manajemen ekstrakurikuler sekolah.

## Setup di Windows (Langkah demi Langkah)

### 1. Clone Repository

Buka terminal/CMD di folder tempat kamu ingin menyimpan project:

```bash
git clone https://github.com/arhylsion/eskul-django.git
cd eskul-django

```

### 2. Setup Virtual Environment

Pastikan Python 3.12+ sudah terinstall:

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Setup Database (Laragon)

1. Buka **Laragon**, klik **Start All**.
2. Buka browser, akses `http://localhost/phpmyadmin/`.
3. Buat database baru dengan nama `eskul_database` (pastikan collation adalah `utf8mb4_general_ci`).
4. Jalankan migrasi untuk membuat struktur tabel:
```bash

```
python manage.py makemigrations
python manage.py migrate

```
5. Jalankan seeder untuk mengisi data awal:
   ```bash
   python eskul_project/seed_data.py

```

### 5. Jalankan Aplikasi

```bash
python manage.py runserver

```

Buka `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)` di browser kamu.

## Akun Login

* **Admin**:
* Username: `admin`
* Password: `admin123`


* **Siswa (49 Akun)**:
* NIS: `2425000` s/d `2425048`
* Password: `password123`