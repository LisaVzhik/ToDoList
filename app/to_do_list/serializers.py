from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Comment


class AuthorSerializer(serializers.ModelSerializer):
    """ Автор задачи """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class TasksSerializer(serializers.ModelSerializer):
    """ Список задач """

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    """ Комментарии """
    author = AuthorSerializer(read_only=True)

    comment_id = serializers.SerializerMethodField('get_comment_id')

    def get_comment_id(self, obj):
        return obj.pk

    class Meta:
        model = Comment
        fields = ('comment_id', 'message', 'date_add', 'author',)


class TaskDetailSerializer(serializers.ModelSerializer):
    """ Одна задача """
    author = AuthorSerializer(read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Task


    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        date_add = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S.%f')
        # Конвертируем дату в строку в новом формате
        ret['date_add'] = date_add.strftime('%d %B %Y %H:%M:%S')
        return ret


class TaskEditorSerializer(serializers.ModelSerializer):
    """ Добавление или изменение задачи """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['date_add', 'author', ]  # Только для чтения


class TaskMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title',)


class CommentAddSerializer(serializers.ModelSerializer):
    """ Добавление комментария """
    author = AuthorSerializer(read_only=True)
    note = TaskMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_add', 'author', 'note']
