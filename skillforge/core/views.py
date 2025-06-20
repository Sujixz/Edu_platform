from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment

User = get_user_model()


def index(request):
    courses = Course.objects.filter(is_published=True)
    enrollments = []

    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'index.html', {
        'courses': courses,
        'enrollments': enrollments
    })


def courses(request):
    all_courses = Course.objects.filter(is_published=True)
    return render(request, 'courses.html', {'courses': all_courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    return render(request, 'core/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
    })


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")
        
        elif username == password1:
            messages.error(request,"Username and Password must be different")
            return render(request,"signup.html")


        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("signin")

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(request, username=user.username, password=password)

            if auth_user:
                login(request, auth_user)
                messages.success(request, "Logged in successfully.")
                return redirect("index")
            else:
                messages.error(request, "Invalid credentials.")
                return render(request, "signin.html")

        except User.DoesNotExist:
            messages.error(request, "No user with this email found.")
            return render(request, "signin.html")

    return render(request, "signin.html")


def userlogout(request):
    logout(request)
    return redirect("index")

# Dashboard View - Show enrolled courses
@login_required
def dashboard(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'dashboard.html', {
        'user': request.user,
        'enrolled_courses': enrolled_courses,
    })


def wishlist(request):
    return render(request, 'wishlist.html')


def search_results(request):
    query = request.GET.get('q', '')
    return render(request, 'search_results.html', {'query': query})


