from django.urls import path

from . import views

app_name = 'to_do_list'
urlpatterns = [
    path('tasks/', views.TasksView.as_view(), name='notes'),  # Список всех задач public=True
    path('task/<int:task_id>/', views.TaskDetailView.as_view(), name='note'),  #

    path('task/add/', views.TaskEditorView.as_view(), name='add'),  # Добавление новой задачи
    path('task/<int:task_id>/save/', views.TaskEditorView.as_view(), name='save'),  # редактирование записи
    path('task/<int:task_id>/del/', views.TaskEditorView.as_view(), name='delete'),  # удаление записи

    path('comment/<int:task_id>/add/', views.CommentDetailView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/del/', views.CommentDetailView.as_view(), name='comment_del'),

]
