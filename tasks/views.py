from django.shortcuts import render
from rest_framework.reverse import reverse
from .models import Task
from tasks.api.views import TaskList
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser



# Create your views here.


def home(request):

	# stream = BytesIO(TaskList.as_view()(request).render().content)
	# data = JSONParser().parse(stream)

	# context = {
	# 	'tasks': data
	# 	}
	context = None
	return render(request, 'index.html', context)