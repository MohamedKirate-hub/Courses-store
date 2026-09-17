from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, F
from item.models import Course, Feedback, Cart, FavoriteItem
from .models import EnrolleCourse, Section, Lecture, CancelEnrolleCourse
from .forms import FeedbackForm, LectureForm

@login_required(login_url='login')
def course_view(request, pk):
    course = get_object_or_404(
        Course.objects.annotate(avg_rates=Avg('ratings__rate')).annotate(rates_count=Count('ratings__rate')),
        id=pk
    )
    feedbacks = Feedback.objects.filter(course=course)
    user_exist = feedbacks.filter(owner = request.user).exists()
    if request.user != course.author:
        Course.objects.filter(id=course.id).update(
            visitor = F('visitor') + 1
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
            return redirect('course-detail', pk=course.id)

    if course.avg_rates is not None:
        course.avg_rates = round(course.avg_rates, 1)

    sections = course.sections.all()
    author_courses = Course.objects.filter(author=course.author, published=True).exclude(id=course.id)
    context = {'course': course, 'author_courses': author_courses,
               'is_enrolled': enrolled,
               'feedback_form': feedback_form,
               'feedbacks': feedbacks,
               "sections": sections,
               'user_exist': user_exist}
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
        CancelEnrolleCourse.objects.create(
            user = request.user,
            course = course
        )
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

@login_required(login_url='login')
def create_section(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.user != course.author:
        return redirect('course-detail', pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            order = course.sections.count()
            Section.objects.create(
                course = course,
                title = title,
                order = order + 1,
            )
        return redirect('course-detail', pk=pk)
    context = {"course": course, 'page': 'create'}
    return render(request, 'course_section.html', context)

@login_required(login_url='login')
def delete_section(request, pk):
    section = get_object_or_404(Section, id=pk)
    course = section.course
    if request.user != course.author:
        return redirect('course-detail', course.id)

    if request.method == 'POST':
        section.delete()
        return redirect('course-detail', course.id)

    context = {'section': section, 'course': course}
    return render(request, 'delete_section.html', context)

@login_required(login_url='login')
def update_section(request, pk):
    section = get_object_or_404(Section, id=pk)
    course = section.course

    if request.user != course.author:
        return redirect('course-detail', pk=course.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            section.title = title.strip()
            section.save()
            return redirect('course-detail', pk=course.id)

    context = {'course': course, 'section': section, 'page': 'update'}
    return render(request, 'course_section.html', context)

@login_required(login_url='login')
def create_lecteur(request, pk):
    section = get_object_or_404(Section, id=pk)
    course = section.course
    form = LectureForm()
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)

        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.section = section
            lecture.order = section.lectures.count() + 1
            lecture.save()
            return redirect('course-detail', pk=course.id)
    context = {'course': course, 'section': section, 'form': form, 'page': 'create'}
    return render(request, 'course_lecteur.html', context)

@login_required(login_url='login')
def lecture_detail(request, pk):

    lecture = get_object_or_404(
        Lecture,
        id=pk
    )

    course = lecture.section.course

    if request.user == course.author:
        pass

    elif not course.enrollments.filter(
        user=request.user
    ).exists():
        return redirect('course-detail', pk=course.id)

    return render(request, 'lecture_detail.html', {
        'lecture': lecture,
        'course': course,
        'section': lecture.section,
    })

