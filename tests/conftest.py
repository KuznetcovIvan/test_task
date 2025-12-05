import pytest
from django.test.client import Client
from django.urls import reverse

from config.celery import app as celery_app
from payouts.models import Payout


@pytest.fixture
def creator(django_user_model):
    return django_user_model.objects.create(username='Creator_user')


@pytest.fixture
def another(django_user_model):
    return django_user_model.objects.create(username='Another_user')


@pytest.fixture
def creater_client(creator):
    client = Client()
    client.force_login(creator)
    return client


@pytest.fixture
def another_client(another):
    client = Client()
    client.force_login(another)
    return client


@pytest.fixture
def payload():
    return {
        'amount': '100.50',
        'currency': 'RUB',
        'beneficiary_name': 'Ivan Petrov',
        'beneficiary_account': '1234567890123456',
        'description': 'Test payout',
    }


@pytest.fixture
def payout(creator, payload):
    return Payout.objects.create(**payload, created_by=creator)


@pytest.fixture
def list_create_payout_url():
    return reverse('payouts-list')


@pytest.fixture
def retrive_update_destroy_url(payout):
    return reverse('payouts-detail', args=[payout.id])


@pytest.fixture(autouse=True)
def enable_celery_eager():
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
