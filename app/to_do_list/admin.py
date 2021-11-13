from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class NoteAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = ('title', 'important', 'date_add', 'status', 'author', 'public')

    # Группировка поля в режиме редактирования
    fields = (('title', 'public'), ('status', 'important'), 'message', 'author', 'date_add')

    # Поля только для чтения в режиме редактирования
    readonly_fields = ('date_add', 'author',)

    # Поиск по выбранным полям
    search_fields = ['title', 'message', ]

    # Фильтры справа
    list_filter = ('public', 'author', 'status', 'important')

    def save_model(self, request, obj, form, change):
        # Добавляем текущего пользователя (если не выбран) при сохранении модели
        # docs: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
