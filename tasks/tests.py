from django.test import TestCase
from .models import Task
from rest_framework.test import APIRequestFactory
from django.utils import timezone
import pytz
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

# Create your tests here.

class OrderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="shahrukh", password="shahrukh", is_staff=True)
        date_1 = timezone.make_aware(timezone.datetime(2018, 11, 12, 2, 3, 5))
        date_2 = timezone.make_aware(timezone.datetime(2018, 10, 12, 2, 3, 5))
        Task.objects.create(user=user, title="Test title 1", due_date=date_1)
        Task.objects.create(user=user, title="Test title 2", due_date=date_2)
        Task.objects.create(user=user, title="Today's work", due_date=timezone.now())

    def test_order(self):
        # checking if the order is according to the due date
        response = client.get(reverse('task-list'))
        qs = response.data["tasks"]
        if qs.exists() and qs.count() >= 2:
            self.assertGreaterEqual(qs[1].due_date, qs[0].due_date)

    def test_deleted_object_fetched(self):
        # checking if deleted tasks are not fetched mistakenly
        response = client.get(reverse('task-list'))
        qs = response.data["tasks"]
        if qs.exists():
            self.assertNotEqual(qs[0].deleted, True)

    def test_filtering_on_duedate_for_today(self):
        response = client.get(reverse('task-list') + "?date=today")
        qs = response.data["tasks"]
        if qs.exists():
            self.assertEqual(qs[0].due_date.date(), timezone.now().date())
        else:
            print("No entries for today found")

    def test_filtering_on_duedate_for_overdue(self):
        response = client.get(reverse('task-list') + "?date=overdue")
        qs = response.data["tasks"]
        if qs.exists():
            self.assertLess(qs[0].due_date.date(), timezone.now().date())
        else:
            print("No entries for today found")

    def test_detail_view(self):
        response = client.get(reverse('task-list'))
        qs = response.data["tasks"]
        if qs.exists():
            response = client.get(reverse('task-detail', kwargs={'pk': qs[0].pk}))
            self.assertEqual(response.data["tasks"][0].pk, qs[0].pk)
