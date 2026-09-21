from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Course, Cart, CardItem, FavoriteItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .forms import CourseForm
from recommendation.recommend_model import RecommendationSystem
from django.contrib.admin.views.decorators import staff_member_required
from .services import import_courses
from django.contrib import messages


def home_page(request):
    query = request.GET.get('query', '')
    model = RecommendationSystem(request.user)

    courses = Course.objects.filter(published=True).filter(
        Q(title__icontains=query) |
        Q(language__icontains=query) |
        Q(topics__name__icontains=query) |
        Q(sections__title__icontains=query) |
        Q(sections__lectures__title__icontains=query)
    ).annotate(avg_rate = Avg('ratings__rate'))
    if request.user.is_authenticated:
        courses = courses.exclude(enrollments__user=request.user)
        recommended_courses = model.recommendation()
    else:
        recommended_courses = []
    courses = courses.order_by('-avg_rate', '-visitor').distinct()  
    context = {'courses': courses,
               'recommended_courses': recommended_courses}

    return render(request, 'home.html', context)

@login_required(login_url='login')
def create_course_view(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            form.save_m2m()

            new_topic_name = form.cleaned_data.get('new_topic')
            if new_topic_name:
                topic, created = Topic.objects.get_or_create(name=new_topic_name.strip())
                course.topics.add(topic)
            return redirect('home')
    context = {'form': form}
    return render(request, 'create.html', context)

@login_required(login_url='login')
def update_course_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            item = form.save()
            new_topic_name = form.cleaned_data.get('new_topic')
            if new_topic_name:
                new_topic_name = new_topic_name.strip()
                topic, created = Topic.objects.get_or_create(name=new_topic_name)
                item.topics.add(topic)
            return redirect('home')
    
    context = {"form": form}
    return render(request, 'update.html', context)

@login_required(login_url='login')
def delete_course_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('home')
    context = {'obj': course}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def add_to_cart_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    favorite_item = FavoriteItem.objects.filter(
        user=request.user,
        course=course).first()

    if favorite_item:
        favorite_item.delete()

    cart, created = Cart.objects.get_or_create(user=request.user)
    CardItem.objects.get_or_create(cart = cart, course = course)
    return redirect('home')

@login_required(login_url='login')
def cart_view(request):
    query = request.GET.get('query', '')
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('course')

    if query:
        items = items.filter(
            Q(course__title__icontains=query) |
            Q(course__language__icontains=query) |
            Q(course__topics__name__icontains=query) |
            Q(course__sections__title__icontains=query) |
            Q(course__sections__lectures__title__icontains=query)
        ).distinct()

    total_price = sum(item.course.get_final_price() for item in items)
    total_price = round(total_price, 2)
    context = {'items': items, 'total_price': total_price}
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def delete_at_cart(request, pk):
    cart_item = get_object_or_404(CardItem, id=pk)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def add_to_favorite_view(request, pk):
    course = get_object_or_404(Course, id=pk)

    FavoriteItem.objects.get_or_create(
        user = request.user, course = course
    )
    return redirect('home')

@login_required(login_url='login')
def favorites_view(request):
    query = request.GET.get('query', '')
    favorite_items = FavoriteItem.objects.filter(
        Q(course__title__icontains=query)|
        Q(course__language__icontains=query)|
        Q(course__topics__name__icontains=query)|
        Q(course__sections__title__icontains=query)|
        Q(course__sections__lectures__title__icontains=query)
    )
    favorite_items = favorite_items.filter(user=request.user).select_related('course').distinct()
    context = {'favorites': favorite_items}
    return render(request, 'favorite.html', context)

@login_required(login_url='login')
def delete_favorite(request, pk):
    favorite_item = get_object_or_404(FavoriteItem, id=pk)
    favorite_item.delete()
    return redirect('favorite')

@login_required(login_url='login')
def move_to_favorite(request, pk):
    course = get_object_or_404(Course, id=pk)
    cart = Cart.objects.get(user=request.user)
    cart_item = cart.items.filter(course=course).first()
    if cart_item:
        cart_item.delete()
    FavoriteItem.objects.update_or_create(user=request.user, course=course)
    return redirect('cart')

@staff_member_required
def import_courses_view(request):
    if request.method == 'POST':
        file = request.FILES.get('csv_file')
        if not file:
            messages.error(request, "Please select a csv file.")
            return redirect('import-courses')
        try:
            imporetd = import_courses(file)
            messages.success(request,
                             f"{imporetd}")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('import-courses')
    return render(request, 'import_courses.html')
