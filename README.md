# Eskul Project

Project manajemen ekstrakurikuler sekolah.

## Setup di Windows
1. Pastikan Python 3.12+ terinstall.
2. Setup Virtual Environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan Seeder (Ini akan membuat database dan akun default):
   ```bash
   python eskul_project/seed_data.py
   ```
5. Jalankan Aplikasi:
   ```bash
   cd eskul_project
   python manage.py runserver
   ```

## Akun Login
- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
- **Siswa (49 Akun)**:
  - NIS: `2425000` s/d `2425048`
  - Password: `password123`
