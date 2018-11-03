from tasks.models import Task, SubTask
from rest_framework import generics
from .serializers import TaskSerializer, SubTaskSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import timedelta



class TaskList(generics.ListCreateAPIView):
	serializer_class = TaskSerializer
	queryset = Task.objects.all().filter(deleted=False)
	renderer_classes = (TemplateHTMLRenderer, )

	def get(self, request, *args, **kwargs):
		qs = self.get_queryset()
		return Response({'tasks': qs}, template_name='index.html')

	def get_queryset(self):
		queryset = Task.objects.all().filter(deleted=False)
		query = self.request.GET.get('query')
		date = self.request.GET.get('date')
		if query:
			queryset = queryset.filter(title__icontains=query)
		if date:
			if date == "today":
				queryset = queryset.filter(due_date__date=timezone.now().date())
			elif date =="overdue":
				queryset = queryset.filter(due_date__date__lt=timezone.now().date())
			elif date =="thisweek":
				queryset = queryset.filter(Q(due_date__date__gte=timezone.now().date()) & Q(due_date__date__lte=timezone.now().date() + timedelta(days=7)))
			elif date =="nextweek":
				queryset = queryset.filter(Q(due_date__date__gt=timezone.now().date() + timedelta(days=7)) & Q(due_date__date__lte=timezone.now().date() + timedelta(days=14)))
		return queryset

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer
	renderer_classes = (TemplateHTMLRenderer, JSONRenderer)

	def get(self, request, *args, **kwargs):
		qs = self.get_object()
		return Response({'tasks': [qs]}, template_name='index.html')


class SubTaskList(generics.ListCreateAPIView):
	queryset = SubTask.objects.all()
	serializer_class = SubTaskSerializer
	renderer_classes = (JSONRenderer, )


class SubTaskDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = SubTask.objects.all()
	serializer_class = SubTaskSerializer



class MarkTaskDone(generics.GenericAPIView):
	queryset = Task.objects.all()
	# renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		task = self.get_object()
		task.done = True
		task.save()
		serializer_context = {
			'request': request,
		}
		content = TaskSerializer(instance=task, context=serializer_context).data
		return Response(content)


class MarkTaskDeleted(generics.GenericAPIView):
	queryset = Task.objects.all()
	# renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		task = self.get_object()
		task.deleted = True
		task.save()
		serializer_context = {
			'request': request,
		}
		content = TaskSerializer(instance=task, context=serializer_context).data
		return Response(content)


class MarkSubTaskDone(generics.GenericAPIView):
	queryset = SubTask.objects.all()
	# renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		subtask = self.get_object()
		subtask.done = True
		subtask.save()
		serializer_context = {
			'request': request,
		}
		content = SubTaskSerializer(instance=subtask, context=serializer_context).data
		return Response(content)
