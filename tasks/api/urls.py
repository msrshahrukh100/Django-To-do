from django.contrib import admin
from django.urls import path, include
from tasks.api.views import (TaskList, TaskDetail, MarkTaskDone, SubTaskList, SubTaskDetail, MarkSubTaskDone, MarkTaskDeleted)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'', TaskList.as_view(), name="task-list"),
    path(r'tasks/', TaskList.as_view(), name="task-list"),
    path(r'tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
	path(r'tasks/<int:pk>/done/', MarkTaskDone.as_view(), name="task-done"),
	path(r'tasks/<int:pk>/delete/', MarkTaskDeleted.as_view(), name="task-delete"),
    path(r'subtasks/', SubTaskList.as_view(), name="subtask-list"),
    path(r'subtasks/<int:pk>/', SubTaskDetail.as_view(), name='subtask-detail'),
    path(r'subtasks/<int:pk>/done/', MarkSubTaskDone.as_view(), name="subtask-done"),

]
