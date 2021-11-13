from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('активно', 'активно'),
    ('отложено', 'отложено'),
    ('выполнено', 'выполнено'),
)


class Task(models.Model):
    """ Задача """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(default='', verbose_name='Текст')
    date_add = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    important = models.BooleanField(default=False, verbose_name='Важно')
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='Автор')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='активно', verbose_name='Статус')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ Комментарии к задаче """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    message = models.TextField(default='', blank=True, verbose_name='Текст комментария')

    def __str__(self):
        return f'{self.message or "Без комментариев"}'
