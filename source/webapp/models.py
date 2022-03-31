from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.urls import reverse
from django_currentuser.middleware import get_current_authenticated_user

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Like(models.Model):
    user = models.ForeignKey(get_user_model(),
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Article(BaseModel):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Контент")
    tags = models.ManyToManyField("webapp.Tag", related_name="articles")
    author = models.ForeignKey(
        User,
        related_name="articles",
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name="Автор",
    )
    likes = GenericRelation(Like)

    def get_object_type(self):
        return ContentType.objects.get_for_model(self)

    def add_like(self):
        obj_type = self.get_object_type()
        Like.objects.get_or_create(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user())

    def delete_like(self):
        obj_type = ContentType.objects.get_for_model(self)
        Like.objects.filter(
            content_type=obj_type, object_id=self.id, user=get_current_authenticated_user()
        ).delete()

    def is_fan(self) -> bool:
        user = get_current_authenticated_user()
        if not user:
            return False
        obj_type = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=self.id, user=user).exists()
        return likes

    def total_likes(self):
        return self.likes.count()

    def make_response(self):
        response = {
            'is_fan': self.is_fan(),
            'total_likes': self.total_likes()
        }
        return response

    def get_absolute_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.pk})

    def upper(self):
        return self.title.upper()

    def __str__(self):
        return f"{self.pk}. {self.author}: {self.title}"

    class Meta:
        db_table = 'articles'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Tag(BaseModel):
    name = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self):
        return f"{self.pk} - {self.name}"

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(BaseModel):
    content = models.TextField(max_length=2000, verbose_name="Контент")
    author = models.ForeignKey(
        User,
        related_name="comments",
        default=1,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    article = models.ForeignKey("webapp.Article", on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name="Статья",
                                )
    likes = GenericRelation(Like)

    @staticmethod
    def get_request_user():
        return get_current_authenticated_user()

    def get_object_type(self):
        return ContentType.objects.get_for_model(self)

    def add_like(self):
        obj_type = self.get_object_type()
        Like.objects.get_or_create(
            content_type=obj_type, object_id=self.id, user=self.get_request_user())

    def make_response(self):
        response = {
            'is_fan': self.is_fan(),
            'total_likes': self.total_likes()
        }
        return response

    def delete_like(self):
        obj_type = ContentType.objects.get_for_model(self)
        Like.objects.filter(
            content_type=obj_type, object_id=self.id, user=self.get_request_user()
        ).delete()

    def is_fan(self) -> bool:
        user = get_current_authenticated_user()
        if not user:
            return False
        obj_type = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=self.id, user=user).exists()
        return likes

    def total_likes(self):
        return self.likes.count()

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
