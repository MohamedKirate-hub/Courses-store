from django.http import HttpResponse
import csv

def export_user_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)

    writer.writerow([
        'ID', 'username', 'first_name', 'last_name', 'email',
        'date_joined',
    ])

    for user in queryset:
        writer.writerow([
            user.id, user.username, user.first_name, user.last_name,
            user.email, user.date_joined
        ])
    return response


def export_course_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'author_username',
        'author_email',
        'title',
        'description',
        'price',
        'topics',
        'language',
        'published',
        'created_at',
        'last_update'
    ])

    for course in queryset:
        topics = ", ".join(
                            topic.name
                            for topic in course.topics.all()
                            )
        writer.writerow(
            [course.id, course.author.username, course.author.email,
            course.title, course.description, course.price,
            topics, course.language, course.published,
            course.created_at, course.updated_at]
        )
    return response
