from rest_framework import serializers
from tasks.models import Task, SubTask

class SubTaskSerializer(serializers.HyperlinkedModelSerializer):
	mark_done = serializers.HyperlinkedIdentityField(view_name='subtask-done')
	class Meta:
		model = SubTask
		fields = ['url', 'task', 'mark_done', 'content', 'done']



class TaskSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	subtasks = SubTaskSerializer(many=True, read_only=True)
	mark_done = serializers.HyperlinkedIdentityField(view_name='task-done')
	mark_deleted = serializers.HyperlinkedIdentityField(view_name='task-delete')

	class Meta:
		model = Task
		fields = ['url', 'user', 'title', 'mark_done', 'mark_deleted', 'subtasks', 'due_date', 'done', 'deleted']