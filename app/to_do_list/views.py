from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import Task, Comment
from .serializers import TasksSerializer, TaskDetailSerializer, TaskEditorSerializer, CommentAddSerializer


class TasksView(APIView):
    """ Список задач """

    def get(self, request):
        """ Получить задачи """

        # Это НЕ оптимизированный запрос
        # param = request.GET
        # print(param['public'])
        # tasks = Task.objects.filter(public=param['public']).filter(important=param['important']).order_by('-date_add', 'title')
        tasks = Task.objects.all().filter(
            Q(public=request.GET['public']) |
            Q(important=request.GET['important'])
        )
        # `select_related` - это оптимизация запроса (join). Отношение Один к Одному
        # https://django.fun/docs/django/ru/3.1/ref/models/querysets/#select-related
        # notes = Note.objects.filter(public=True).order_by('-date_add', 'title').select_related('author')
        # notes = notes.only('id', 'title', 'message', 'date_add', 'author__username')

        # print(notes.query)
        # logger.debug(notes.query)

        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data)


class TaskDetailView(APIView):
    """ Задача """

    def get(self, request, task_id):
        """ Получить задачу """

        # Это НЕ оптимизированный запрос
        task = Task.objects.filter(pk=task_id, public=True).first()

        # `prefetch_related` - это оптимизация запроса для отношения Многие к Одному
        # https://django.fun/docs/django/ru/3.1/ref/models/querysets/#prefetch-related
        # note = Note.objects.select_related(
        #     'author'
        # ).prefetch_related(
        #     'comments'
        # ).filter(
        #     pk=note_id, public=True
        # ).first()

        if not task:
            raise NotFound(f'Опубликованная статья с id={task_id} не найдена')

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class TaskEditorView(APIView):
    """ Добавление, изменение или удаление задачи """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Новая статья для блога """

        # Передаем в сериалайзер (валидатор) данные из запроса
        new_task = TaskEditorSerializer(data=request.data)

        # Проверка параметров
        if new_task.is_valid():
            # Записываем новую статью и добавляем текущего пользователя как автора
            new_task.save(author=request.user)
            return Response(new_task.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_task.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):

        # Находим редактируемую статью
        task = Task.objects.filter(pk=task_id, author=request.user).first()
        if not task:
            raise NotFound(f'Статья с id={task_id} для пользователя {request.user.username} не найдена')

        # Для сохранения изменений необходимо передать 3 параметра
        # Объект связанный со статьей в базе: `note`
        # Изменяемые данные: `data`
        # Флаг частичного оновления (т.е. можно проигнорировать обязательные поля): `partial`
        new_task = TaskEditorSerializer(task, data=request.data, partial=True)

        if new_task.is_valid():
            new_task.save()
            return Response(new_task.data, status=status.HTTP_200_OK)
        else:
            return Response(new_task.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        """ Удалить задачу """
        task = Task.objects.filter(pk=task_id, author=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentDetailView(APIView):
    """ Комментарий к задаче """
    permission_classes = (IsAuthenticated,)

    def post(self, request, task_id):
        """ Новый комментарий """

        task = Task.objects.filter(pk=task_id).first()
        if not task:
            raise NotFound(f'Статья с id={task_id} не найдена')

        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(note=task, author=request.user)
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """ Удалить комментарий """
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
