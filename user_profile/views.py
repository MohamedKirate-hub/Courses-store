from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from account_auth.models import User
from .forms import UserForm
from django.db.models import Q

@login_required(login_url='login')
def profile_view(request, pk):
    user = get_object_or_404(User, id=pk)
    courses = user.courses.all()
    query = request.GET.get('query', '')
    course_filter = request.GET.get('filter', 'all')

    if request.user != user:
        courses = courses.filter(published=True)

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(language__icontains=query) |
            Q(topics__name__icontains=query) |
            Q(sections__title__icontains=query) |
            Q(sections__lectures__title__icontains=query)
        ).distinct()

    if request.user == user:

        if course_filter == 'published':
            courses = courses.filter(published=True)

        elif course_filter == 'draft':
            courses = courses.filter(published=False)

    context = {
        'user': user,
        'courses': courses,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def update_profile_view(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk)
    context = {'form': form}
    return render(request, 'edite.html', context)