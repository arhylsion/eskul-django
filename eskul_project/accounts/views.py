from django.shortcuts import render, redirect
from .models import Student

def login_view(request):

    if request.method == 'POST':

        nis = request.POST.get('nis')
        password = request.POST.get('password')

        try:

            student = Student.objects.get(
                nis=nis,
                password=password
            )

            request.session['student_id'] = student.id
            request.session['student_name'] = student.nama

            return redirect('registration_form')

        except Student.DoesNotExist:

            return render(request, 'login.html', {
                'error': 'NIS atau Password salah!'
            })

    return render(request, 'login.html')

def logout_view(request):

    request.session.flush()

    return redirect('login')
