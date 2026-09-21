from django.contrib import admin, messages
from account_auth.models import User
from course.models import EnrolleCourse, CancelEnrolleCourse
from item.models import Course, Topic, Feedback
from .forms import CourseAdminForm
from django.db.models import Avg, Count, Prefetch, F
from django.db.models.functions import Upper, Lower, Substr, Concat
from .utils import export_user_csv, export_course_csv
from django.urls import path
from . import views


class CustomAdminSite(admin.AdminSite):

    site_header = "Course Platform Administration"
    site_title = "Course Platform Admin"
    index_title = "Welcome to the Course Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-courses/', views.import_courses_view, name='import-courses')
        ]
        return custom_urls + urls


admin_site = CustomAdminSite(name='custom_admin')

# Course page


class FeedbackInline(admin.StackedInline):
    model = Feedback
    extra = 1


class PriceFilter(admin.SimpleListFilter):

    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('cheap', 'Cheap courses (≤ $5)'),
            ('medium', 'Medium courses ($5–$10)'),
            ('expensive', 'Expensive courses (> $10)'),
        )

    def queryset(self, request, queryset):

        value = self.value()

        if value == 'cheap':
            return queryset.filter(
                price__lte=5
            )

        if value == 'medium':
            return queryset.filter(
                price__gt=5,
                price__lte=10
            )

        if value == 'expensive':
            return queryset.filter(
                price__gt=10
            )

        return queryset


@admin.action(description="Publish selected courses")
def publish_courses(modeladmin, request, queryset):
  unpublished_courses = queryset.filter(published=False)
  count = unpublished_courses.update(published=True)
  messages.success(request, f"{count} courses were successfully published.")

@admin.action(description="Unpublish selected courses")
def unpublish_courses(modeladmin, request, queryset):
    publihsed_courses = queryset.filter(published=True)
    count = publihsed_courses.update(published=False)
    messages.success(request, f"{count} courses were successfully unpublished.")

@admin.register(Course, site=admin_site)
class CourseAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/course_admin.css',)
        }
    change_list_template = 'admin/item/course/change_list.html'

    readonly_fields = ('updated_at', 'created_at', 'visitor')
    list_display = ('author_username', 'title', 'description', 'published',
                    'language', 'topics_list', 'price', 'avg_rate')
    list_filter = ('published', 'language', PriceFilter)
    search_fields = ('author__username', 'title')
    ordering = ('-created_at',)
    list_per_page = 4

    @admin.display(description='Topics List')
    def topics_list(self, obj):
        return ', '.join( topic.name for topic in obj.topics.all())

    @admin.display(description='Author Username')
    def author_username(self, obj):
        return obj.author.username

    @admin.display(description='Average rate')
    def avg_rate(self, obj):
        if obj.avg_rate is None:
            return 'Not rated'
        return '★' * int(obj.avg_rate) + '☆' * int(5 - obj.avg_rate)

    filter_horizontal = (
        'topics',
    )
    date_hierarchy = 'created_at'
    actions = (
        publish_courses, unpublish_courses, export_course_csv
    )

    form = CourseAdminForm
    inlines = (FeedbackInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(avg_rate = Avg('ratings__rate'))

# Topic page

class AppearanceFilter(admin.SimpleListFilter):
    title = 'Course Appearance'
    parameter_name = 'appearance'

    def lookups(self, request, model_admin):
        return (
            ('most', 'Most courses'),
            ('least', 'Least courses'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'most':
            return queryset.order_by('-appearance')
        if self.value() == 'least':
            return queryset.order_by('appearance')
        return queryset

@admin.register(Topic, site=admin_site)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'appearance_count', 'average_price')
    search_fields = ('name',)
    list_filter = (AppearanceFilter,)
    list_per_page = 5

    @admin.display(description='Courses',
                   ordering='appearance')
    def appearance_count(self, obj):
        return obj.appearance

    @admin.display(
        description='Average Price',
        ordering='price_avg'
    )
    def average_price(self, obj):
        if obj.price_avg is None:
            return '—'
        return f"${obj.price_avg:.2f}"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            appearance = Count('courses', distinct=True),
            price_avg = Avg('courses__price')
        )

#Feedback

class FeedbackRateFilter(admin.SimpleListFilter):
    title = 'Feedback Rate'
    parameter_name = 'feedback_rate'

    def lookups(self, request, model_admin):
        return (
            ('five', '5 stars'),
            ('four', '4 stars'),
            ('three', '3 stars'),
            ('two', '2 stars'),
            ('one', '1 star'),
            ('unrated', 'Not rated'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'five':
            return queryset.filter(rate=5)

        if self.value() == 'four':
            return queryset.filter(rate=4)

        if self.value() == 'three':
            return queryset.filter(rate=3)

        if self.value() == 'two':
            return queryset.filter(rate=2)

        if self.value() == 'one':
            return queryset.filter(rate=1)

        if self.value() == 'unrated':
            return queryset.filter(rate__isnull=True)

        return queryset

@admin.register(Feedback, site=admin_site)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('title_display', 'owner_username', 'course_author',
                    'created_at', 'updated_at',
                    'feedback_content', 'rating_display',)
    search_fields = ('content', 'course__title', 'course__author__username',
                     'owner__email', 'owner__username')
    list_per_page = 20
    list_filter = (FeedbackRateFilter,)
    date_hierarchy = 'created_at'

    @admin.display(description='Course Title')
    def title_display(self, obj):
        if len(obj.course.title) < 15:
            return obj.course.title
        return f"{obj.course.title[:15]}..."

    @admin.display(description='Course author')
    def course_author(self, obj):
        return obj.course.author.username

    @admin.display(description='Owner Username')
    def owner_username(self, obj):
        return obj.owner.username

    @admin.display(description='Feedback Content')
    def feedback_content(self, obj):
        if len(obj.content) > 20:
            return f"{obj.content[:20]}..."
        return obj.content

    @admin.display(description='Rating', ordering='rate')
    def rating_display(self, obj):
        if obj.rate is None:
            return 'Not rated'
        return '★' * obj.rate + '☆' * (5 - obj.rate)

    def get_queryset(self, request):
        return (super().get_queryset(request).select_related('course',
                                                             'course__author',
                                                             'owner'))

# Enrollements

@admin.action(description='Cancel selected enrollments')
def cancel_enrollements(modeladmin, request, queryset):
    cancelled = 0
    for enrollment in queryset:
        CancelEnrolleCourse.objects.create(
            user = enrollment.user,
            course = enrollment.course
        )
        enrollment.delete()
        cancelled += 1
    messages.success(
        request,
        f'{cancelled} enrollment(s) cancelled successfully.'
    )

@admin.register(EnrolleCourse, site=admin_site)
class EnrollementAdmin(admin.ModelAdmin):
    readonly_fields = ('enrolled_at',)
    list_display = ('course_title', 'user_username', 'rate',
                    'course_price', 'enrolled_at',)
    actions = (cancel_enrollements, )
    date_hierarchy = 'enrolled_at'
    list_per_page = 10
    search_fields = ('course__title', 'course__author__username',
                     'user__username', 'course__description')
    ordering = ('-enrolled_at',)

    @admin.display(description='Course Title')
    def course_title(self, obj):
        if len(obj.course.title) < 15:
            return obj.course.title
        return f"{obj.course.title[:15]}..."

    @admin.display(description='rate')
    def rate(self, obj):
        if obj.avg_rate is None:
            return 'Not rated'
        return '★' * int(obj.avg_rate) + '☆' * int(5 - obj.avg_rate)

    @admin.display(description='Course Price')
    def course_price(self, obj):
        if obj.course.price is None:
            return '—'
        return f"${obj.course.price:.2f}"

    @admin.display(description='Username')
    def user_username(self, obj):
        return obj.user.username

    def get_queryset(self, request):
        return (super().get_queryset(request).select_related('course',
                                                             'course__author',
                                                             'user').annotate(
                                                                 avg_rate = Avg('course__ratings__rate')))

# User

def name_uppercase(modeladmin, request, queryset):
    count = queryset.update(
            first_name = Upper(F('first_name')),
            last_name = Upper(F('last_name')),
        )
    messages.success(
        request,
        f'{count} names were converted to uppercase.'
    )

def name_lowercase(modeladmin, request, queryset):
    count = queryset.update(
        first_name = Lower(F('first_name')),
        last_name = Lower(F('last_name')),
    )
    messages.success(
        request,
        f'{count} names were converted to lowercase.'
    )

def name_capitalize(modeladmin, request, queryset):
    count = queryset.update(
        first_name=Concat(
            Upper(Substr(F('first_name'), 1, 1)),
            Lower(Substr(F('first_name'), 2)),
        ),
        last_name=Concat(
            Upper(Substr(F('last_name'), 1, 1)),
            Lower(Substr(F('last_name'), 2)),
        ),
    )
    messages.success(
        request,
        f'{count} names were capitalized.'
    )

@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined',)
    list_display = ('username', 'last_name', 'first_name',
                    'enrolled_courses', 'cancelled_enrolled_courses',
                    'created_courses',
                    'email', 'user_revenue',
                    'is_staff', 'is_active')

    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'last_name', 'first_name', 'email')
    actions = (name_capitalize, name_lowercase, name_uppercase, export_user_csv)

    @admin.display(description='Courses Created')
    def created_courses(self, obj):
        return obj.courses_created

    @admin.display(description='Enrolled Courses')
    def enrolled_courses(self, obj):
        return obj.enrolled_courses

    @admin.display(description='Cancelled Courses')
    def cancelled_enrolled_courses(self, obj):
        return obj.cancelled_enrolled_courses

    @admin.display(description='User revenue')
    def user_revenue(self, obj):
        revenue = sum(
            course.get_final_price() * (course.enrollments.count() +
                                        course.cancelled_enrollments.count())
            for course in obj.courses.all()
        )
        return f"${revenue:.2f}"

    def get_queryset(self, request):
        courses = Course.objects.annotate(
            enrollment_count=Count('enrollments', distinct=True),
            cancelled_enrollment_count=Count(
                'cancelled_enrollments',
                distinct=True
            )
        )
        return super().get_queryset(request).annotate(
            courses_created = Count('courses', distinct=True),
            enrolled_courses = Count('enrollments', distinct=True),
            cancelled_enrolled_courses = Count('cancelled_enrollments', distinct=True)
        ).prefetch_related(Prefetch('courses', queryset=courses))
