from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.shortcuts import render

from .models import Task, Comment
from .serializers import TasksSerializer, TaskDetailSerializer, TaskEditorSerializer, CommentAddSerializer


class TasksView(APIView):
    """ Список задач """

    def get(self, request):
        """ Получить задачи """
        tasks = Task.objects.filter(a).order_by('-date_add', 'title').select_related('author')

        a = Q(public=True)
        if request.GET['important']:
            tasks = tasks.filter(important=request.GET['important']).fi, important2=request.GET['important'])
            # a = a | Q(important=True)


        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data)


class TaskDetailView(APIView):
    """ Задача """

    def get(self, request, task_id):
        """ Получить задачу """

        task = Task.objects.select_related(
            'author'
        ).prefetch_related(
            'comments'
        ).filter(
            pk=task_id, public=True
        ).first()

        if not task:
            raise NotFound(f'Опубликованная статья с id={task_id} не найдена')

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class TaskEditorView(APIView):
    """ Добавление, изменение или удаление задачи """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Новая задача """

        new_task = TaskEditorSerializer(data=request.data)

        if new_task.is_valid():
            new_task.save(author=request.user)
            return Response(new_task.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_task.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):
        """Обновление задачи"""
        task = Task.objects.filter(pk=task_id, author=request.user).first()
        if not task:
            raise NotFound(f'Задача с id={task_id} для пользователя {request.user.username} не найдена')

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
