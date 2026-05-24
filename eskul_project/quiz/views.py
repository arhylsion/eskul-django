from django.shortcuts import render, redirect
from .models import Question, QuizResult
from accounts.models import Student
from eskul.models import Registration

def quiz_page(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    existing_reg = Registration.objects.filter(student=student).first()
    if not existing_reg:
        return redirect('registration_form')

    last_result = QuizResult.objects.filter(student=student).last()
    if last_result and not last_result.can_retry:
        return redirect('registration_form')

    questions = Question.objects.all()

    if request.method == 'POST':
        total_score = 0
        for question in questions:
            answer = request.POST.get(str(question.id))
            if answer == question.jawaban_benar:
                total_score += question.point

        QuizResult.objects.create(student=student, score=total_score)

        return render(request, 'quiz_result.html', {'score': total_score, 'student': student})

    return render(request, 'quiz.html', {'questions': questions, 'student': student})
