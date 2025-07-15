from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

# Create your views here.

def teacher_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, "portal/login.html", {"error": "Invalid credentials"})
    return render(request, "portal/login.html")

@login_required
def teacher_logout(request):
    logout(request)
    return redirect("/")

@login_required
def dashboard(request):
    form = StudentForm()
    students = Student.objects.all()
    return render(request, "portal/dashboard.html", {"students": students, "form": form})

@login_required
@require_POST
def add_or_update_student(request):
    form = StudentForm(request.POST)
    if form.is_valid():
        try:
            data = form.cleaned_data
            student, created = Student.objects.get_or_create(
                name=data['name'], subject=data['subject'],
                defaults={'marks': data['marks']}
            )
            if not created:
                student.marks += data['marks']
                student.save()
            return JsonResponse({'status': 'success'})
        except ValidationError as e:
            return JsonResponse({"status": "fail", "error": str(e)}, status=400)
    else:
        return JsonResponse({'status': 'fail', 'errors': form.errors}, status=400)

@login_required
@require_POST
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
        try:
            conflict = Student.objects.filter(name=form.cleaned_data["name"],
                                              subject=form.cleaned_data["subject"]
                                              ).exclude(id=student_id).exists()
            if conflict:
                return JsonResponse(
                    {"status": "fail", "error": "Another student with this name and subject already exists."},
                    status=400)

            form.save()
            return JsonResponse({'status': 'updated'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({'status': 'deleted'})