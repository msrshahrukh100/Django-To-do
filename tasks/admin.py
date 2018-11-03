from django.contrib import admin
import tasks.models as tasks_models
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
	list_display = ['title', 'due_date', 'done', 'deleted']

	class Meta:
		model = tasks_models.Task


class SubTaskAdmin(admin.ModelAdmin):
	list_display = ['task', 'content', 'done']

	class Meta:
		model = tasks_models.SubTask


admin.site.register(tasks_models.Task, TaskAdmin)
admin.site.register(tasks_models.SubTask, SubTaskAdmin)
