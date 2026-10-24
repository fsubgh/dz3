from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Count


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class EventQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def popular(self, min_participants=5):
        return self.annotate(
            participants_count=Count(
                'participants',
                distinct=True
            )
        ).filter(
            participants_count__gt=min_participants
        )

    def with_details(self):
        return self.select_related(
            'author'
        ).prefetch_related(
            'categories',
            'participants'
        )

    def recent(self):
        return self.order_by('-created_at')


class Event(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Автор'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='events',
        verbose_name='Категории'
    )
    participants = models.ManyToManyField(
        User,
        related_name='joined_events',
        blank=True,
        verbose_name='Участники'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена'
    )
    max_participants = models.PositiveIntegerField(
        verbose_name='Максимальное количество участников'
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.title
