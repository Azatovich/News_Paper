from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            posts_rating_sum=Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Sum('comment_rating'))

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    
    category_name = models.CharField(max_length=25,default='NW', unique=True)

    def __str__(self):
        return self.category_name

class Post(models.Model):

    ART = 'AR'
    NEWS = 'NW'

    TYPES = [(ART, 'Статья'), (NEWS, 'Новость')]


    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    post_type = models.CharField(max_length=10, choices=TYPES, verbose_name='Тип поста')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    post_category = models.ManyToManyField(Category)

    post_title = models.CharField(max_length=120, verbose_name='Заголовок')

    post_text = models.TextField(verbose_name='Содержание')

    post_rating = models.IntegerField(default=0, verbose_name='Рейтинг поста')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'

    def __str__(self):
        return f'{self.post_title} : {self.post_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):

    category_PostCategory = models.ManyToManyField(Category)
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):


    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_text = models.CharField(max_length=255, null=True)

    time_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
