from django.shortcuts import render, redirect
from .models import Extracurricular, Registration
from accounts.models import Student
from quiz.models import QuizResult

def registration_form(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    existing_reg = Registration.objects.filter(student=student).first()
    result = QuizResult.objects.filter(student=student).last()

    def render_already(msg):
        return render(request, 'already_registered.html', {
            'message': msg,
            'student': student,
            'registration': existing_reg,
            'result': result
        })

    if student.has_eskul:
        return render_already('Anda sudah terdaftar dan diterima dalam ekstrakurikuler.')

    if existing_reg:
        if result:
            if result.score > 70:
                if existing_reg.status == 'approved':
                    return render_already('Anda sudah terdaftar dan diapprove.')
                else:
                    return render_already('Nilai kuis Anda memenuhi kriteria. Menunggu validasi admin.')
            else:
                if not result.can_retry:
                    return render_already('Nilai kuis Anda belum memenuhi kriteria. Menunggu keputusan admin.')

    eskul_list = Extracurricular.objects.all()

    if request.method == 'POST':
        eskul_id = request.POST.get('eskul')
        notes = request.POST.get('notes')
        eskul = Extracurricular.objects.get(id=eskul_id)

        if existing_reg:
            existing_reg.eskul = eskul
            existing_reg.notes = notes

            existing_reg.status = 'pending'
            existing_reg.save()
        else:
            Registration.objects.create(student=student, eskul=eskul, notes=notes)

        if result and result.can_retry:
            result.delete()

        return redirect('quiz_page')

    return render(request, 'registration_form.html', {'student': student, 'eskul_list': eskul_list, 'existing_reg': existing_reg})
