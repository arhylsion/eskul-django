from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Student
from eskul.models import Extracurricular, Registration
from quiz.models import QuizResult
from django.db.models import Count
import csv
import json
from django.db.models.functions import TruncDate

def admin_required(view_func):

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            from django.contrib.auth import views as auth_views
            return redirect(f'/admin/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def dashboard_home(request):
    total_students = Student.objects.count()
    total_registrants = Registration.objects.count()
    popular_eskul = Extracurricular.objects.annotate(num_reg=Count('registration')).order_by('-num_reg').first()
    pending_reviews = Registration.objects.filter(status='pending').count()

    students_with_reg = Student.objects.filter(registration__isnull=False).distinct().count()
    students_without_reg = total_students - students_with_reg

    eskul_distribution = Extracurricular.objects.annotate(num_reg=Count('registration')).order_by('-num_reg')

    max_reg = 1
    if eskul_distribution and len(eskul_distribution) > 0:
        max_reg = max([e.num_reg for e in eskul_distribution])
        if max_reg == 0:
            max_reg = 1

    recent_registrations = Registration.objects.all().order_by('-created_at')[:5]

    context = {
        'total_registrants': total_registrants,
        'total_students': total_students,
        'students_with_reg': students_with_reg,
        'students_without_reg': students_without_reg,
        'popular_eskul': popular_eskul,
        'pending_reviews': pending_reviews,
        'eskul_distribution': eskul_distribution,
        'max_reg': max_reg,
        'recent_registrations': recent_registrations
    }
    return render(request, 'admin_dashboard.html', context)

@admin_required
def dashboard_registrant(request):
    registrations = Registration.objects.all().order_by('-created_at')
    results = QuizResult.objects.all()

    reg_data = []
    for reg in registrations:
        result = results.filter(student=reg.student).last()
        reg_data.append({
            'reg': reg,
            'result': result
        })

    unregistered = Student.objects.filter(registration__isnull=True).order_by('nama')

    return render(request, 'admin_registrant.html', {
        'reg_data': reg_data,
        'unregistered': unregistered,
    })

@admin_required
def approve_registrant(request, reg_id):
    reg = Registration.objects.get(id=reg_id)
    reg.status = 'approved'
    reg.save()

    student = reg.student
    student.has_eskul = True
    student.save()

    return redirect('dashboard_registrant')

@admin_required
def trigger_retry(request, result_id):
    result = QuizResult.objects.get(id=result_id)
    result.can_retry = True
    result.save()
    return redirect('dashboard_registrant')

@admin_required
def dashboard_statistics(request):
    eskul_dist = list(Extracurricular.objects.annotate(num_reg=Count('registration')).order_by('-num_reg'))
    eskul_labels = [e.nama_eskul for e in eskul_dist]
    eskul_data = [e.num_reg for e in eskul_dist]

    time_series = Registration.objects.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
    time_labels = [ts['date'].strftime('%b %d') for ts in time_series]
    time_data = [ts['count'] for ts in time_series]

    score_data = [
        QuizResult.objects.filter(score__lte=50).count(),
        QuizResult.objects.filter(score__gt=50, score__lte=70).count(),
        QuizResult.objects.filter(score__gt=70, score__lte=90).count(),
        QuizResult.objects.filter(score__gt=90).count(),
    ]
    score_labels = ['<= 50', '51 - 70', '71 - 90', '> 90']

    context = {
        'eskul_labels': json.dumps(eskul_labels),
        'eskul_data': json.dumps(eskul_data),
        'time_labels': json.dumps(time_labels),
        'time_data': json.dumps(time_data),
        'score_labels': json.dumps(score_labels),
        'score_data': json.dumps(score_data),
    }
    return render(request, 'admin_statistics.html', context)

@admin_required
def dashboard_settings(request):
    return render(request, 'admin_settings.html')

@admin_required
def export_to_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_siswa.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nama Siswa', 'NIS', 'Kelas', 'Eskul', 'Status', 'Nilai Terakhir', 'Tanggal Mendaftar'])

    registrations = Registration.objects.all()
    for reg in registrations:
        result = QuizResult.objects.filter(student=reg.student).last()
        score = result.score if result else 'N/A'
        writer.writerow([
            reg.student.nama,
            reg.student.nis,
            reg.student.kelas,
            reg.eskul.nama_eskul,
            reg.status,
            score,
            reg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response
