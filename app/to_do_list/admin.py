from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class NoteAdmin(admin.ModelAdmin):

    list_display = ('title', 'important', 'date_add', 'status', 'author', 'public')
    fields = (('title', 'public'), ('status', 'important'), 'message', 'author', 'date_add')
    readonly_fields = ('date_add',)
    search_fields = ['title', 'message', ]
    list_filter = ('public', 'author', 'status', 'important')

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
