from django.db import models
from item.models import User, Course

class EnrolleCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course_enrollment',
            )
        ]

class CancelEnrolleCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='cancelled_enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
        related_name='cancelled_enrollments'
    )
    cancelled_at = models.DateTimeField(auto_now_add=True)

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
         ordering = ['order']

    def __str__(self):
        return self.title

class Lecture(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=250)
    video = models.FileField(upload_to='courses/Videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='courses/pdfs/', blank=True, null=True)
    duration = models.PositiveIntegerField(default=0, help_text="Duration in seconds")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
             ordering = ['order']

    def __str__(self):
            return self.title

