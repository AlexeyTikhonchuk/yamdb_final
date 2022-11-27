from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import CustomUserManager
from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, ' Модератор'),
        (ADMIN, 'Администратор')
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Имя пользователя'
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default=USER,
        verbose_name='Статус'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = CustomUserManager()

    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    def is_moderator(self):
        return self.role == User.MODERATOR


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название категории",
        help_text="Введите название категории"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Адрес страницы категории",
        help_text="Введите адрес для страницы категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название жанра",
        help_text="Введите название жанра"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Адрес страницы жанра",
        help_text="Введите адрес для страницы жанра",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название произведения",
        help_text="Введите название произведения"
    )
    year = models.IntegerField(
        verbose_name="Год",
        validators=(validate_year,),
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        related_name="title",
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="title",
        verbose_name="Жанр"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведения",
        related_name="reviews"
    )
    text = models.TextField(
        verbose_name="Текст"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        related_name="reviews"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Введите число не меньше 1'),
            MaxValueValidator(10, message='Введите число не больше 10')]
    )

    class Meta:
        verbose_name = "Отзыв"
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name="Отзыв",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.CharField(
        max_length=500,
        verbose_name="Текст"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
