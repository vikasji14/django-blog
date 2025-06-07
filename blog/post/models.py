from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_draft = models.CharField(
        max_length=15,
        choices=(
            ('False', 'Draft'),
            ('True', 'Published'),
        ),
        default='True',
    )

    sheduled_date = models.DateTimeField(null=True, blank=True)
    

class PostLike(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_count = models.PositiveBigIntegerField(null=True, editable=True, default=0)

    