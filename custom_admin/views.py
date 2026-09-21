from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from ..item.services import import_courses
from django.contrib import messages

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
