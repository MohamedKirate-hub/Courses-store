from django.http import HttpResponse
import csv

def export_user_csv(modeladmin, request, queryset):
    response = HttpResponse(content='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)

    writer.writerow([
        'ID', 'username', 'first_name', 'last_name', 'email','date_joined',
    ])

    for user in queryset:
        writer.writerow([
            user.id, user.username, user.first_name, user.last_name,
            user.email, user.date_joined
        ])
    return response