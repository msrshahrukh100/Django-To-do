from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import timedelta
from django.utils import timezone
from django.db.models import Q

# Create your models here.


class Task(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')
	title = models.CharField(max_length=255)
	due_date = models.DateTimeField()
	done = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)

	class Meta:
		ordering = ['due_date']

	def __str__(self):
		return self.title

	def get_delete_url(self):
		return reverse("task-delete", kwargs={"pk": self.id})

	def get_done_url(self):
		return reverse("task-done", kwargs={"pk": self.id})

class SubTask(models.Model):
	task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
	content = models.CharField(max_length=255)
	done = models.BooleanField(default=False)

	def __str__(self):
		return str(self.task)


@receiver(post_save, sender=Task)
def delete_old_tasks(sender, instance, **kwargs):
	qs = Task.objects.filter(Q(due_date__date__lt=timezone.now().date() - timedelta(days=30)) & Q(deleted=True))
	for i in qs:
		i.delete()
