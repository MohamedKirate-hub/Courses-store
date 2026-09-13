from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from item.models import Course, Feedback, Cart, FavoriteItem
from .models import EnrolleCourse
from .forms import FeedbackForm

@login_required(login_url='login')
def course_view(request, pk):
    course = get_object_or_404(
        Course.objects.annotate(avg_rates=Avg('ratings__rate')).annotate(rates_count=Count('ratings__rate')),
        id=pk
    )
    enrolled = course.enrollments.filter(user = request.user).exists()
    feedback_form = FeedbackForm()
    if request.method == 'POST' and enrolled:
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            Feedback.objects.update_or_create(
                owner = request.user,
                course = course,
                defaults = {
                    'content': feedback_form.cleaned_data.get('content'),
                    'rate': feedback_form.cleaned_data.get('rate')
                }
            )

    if course.avg_rates is not None:
        course.avg_rates = round(course.avg_rates, 1)

    author_courses = Course.objects.filter(author=course.author).exclude(id=course.id)
    context = {'course': course, 'author_courses': author_courses,
               'is_enrolled': enrolled,
               'feedback_form': feedback_form,}
    return render(request, 'course_view.html', context)

@login_required(login_url='login')
def enrolle_course_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.user == course.author:
        pass
    favorite_item = FavoriteItem.objects.filter(
        user= request.user, course=course
    ).first()
    if favorite_item:
        favorite_item.delete()
    # then check wallete
    enrollement, created = EnrolleCourse.objects.get_or_create(
        user = request.user,
        course = course,
    )
    return redirect('course-detail', pk=pk)

@login_required(login_url='login')
def unenrolle_course_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    enrolled_courses = get_object_or_404(EnrolleCourse,
                                         course=course,
                                         user = request.user)
    if request.method == 'POST':
        enrolled_courses.delete()
        return redirect('learning')
    context = {'course': course}
    return render(request, 'unenroll.html', context)
    

@login_required(login_url='login')
def learning_view(request):
    enrollments = EnrolleCourse.objects.filter(user=request.user).select_related('course')
    context = {
        'enrollments': enrollments
    }
    return render(request, 'learning.html', context)

@login_required(login_url='login')
def enroll_courses(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('course')
    for item in cart_items:
        EnrolleCourse.objects.get_or_create(
            user=request.user,
            course = item.course
        )
    cart.items.all().delete()
    return redirect('learning')
