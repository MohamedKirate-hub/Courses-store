from decimal import Decimal
from django.db import models
from account_auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=255, default='English')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    topics = models.ManyToManyField(Topic, related_name='courses', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,
                                validators=[
                                    MinValueValidator(0)
                                ])
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100),
                                   ])
    visitor = models.PositiveIntegerField(default=0)
    bestseller = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_final_price(self):
        final_price = self.price * (Decimal('1') - self.discount / Decimal('100'))
        return final_price
    def __str__(self):
        return self.title

class Feedback(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    rate = models.PositiveSmallIntegerField(null=True, blank=True,
                                            validators=[
                                                MinValueValidator(1),
                                                MaxValueValidator(5)
                                            ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'course'],
                name='unique_feedback_per_user_course'
            )
        ]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

class CardItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_items')
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'course'],
                                    name='unique_course_in_cart')
        ]

class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'course'],
                name='unique_favorite_per_user_in_course'
            )
        ]
