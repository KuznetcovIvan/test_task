from decimal import Decimal
from http import HTTPStatus

import pytest

from payouts.models import Payout

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_fixture, http_method, client_fixture, expected_status',
    (
        ('list_create_payout_url', 'get', 'client', HTTPStatus.FORBIDDEN),
        ('list_create_payout_url', 'post', 'client', HTTPStatus.FORBIDDEN),
        ('retrive_update_destroy_url', 'get', 'client', HTTPStatus.FORBIDDEN),
        ('retrive_update_destroy_url', 'patch', 'client', HTTPStatus.FORBIDDEN),
        ('retrive_update_destroy_url', 'delete', 'client', HTTPStatus.FORBIDDEN),
        ('list_create_payout_url', 'get', 'creater_client', HTTPStatus.OK),
        ('list_create_payout_url', 'post', 'creater_client', HTTPStatus.CREATED),
        ('retrive_update_destroy_url', 'get', 'creater_client', HTTPStatus.OK),
        ('retrive_update_destroy_url', 'patch', 'creater_client', HTTPStatus.OK),
        ('retrive_update_destroy_url', 'delete', 'creater_client', HTTPStatus.NO_CONTENT),
        ('list_create_payout_url', 'get', 'another_client', HTTPStatus.OK),
        ('list_create_payout_url', 'post', 'another_client', HTTPStatus.CREATED),
        ('retrive_update_destroy_url', 'get', 'another_client', HTTPStatus.NOT_FOUND),
        ('retrive_update_destroy_url', 'patch', 'another_client', HTTPStatus.NOT_FOUND),
        ('retrive_update_destroy_url', 'delete', 'another_client', HTTPStatus.NOT_FOUND),
    ),
)
def test_endpoints_availability(request, url_fixture, http_method, client_fixture, expected_status, payload):
    client = request.getfixturevalue(client_fixture)
    url = request.getfixturevalue(url_fixture)
    method = getattr(client, http_method)
    kwargs = {}
    if http_method in ('post', 'put', 'patch'):
        kwargs = {'data': payload, 'content_type': 'application/json'}
    response = method(url, **kwargs)
    assert response.status_code == expected_status


def test_payout_created_successfully(creater_client, list_create_payout_url, payload, creator):
    response = creater_client.post(list_create_payout_url, data=payload, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED
    assert Payout.objects.count() == 1
    payout = Payout.objects.get()
    assert payout.amount == Decimal(payload['amount'])
    assert payout.currency == payload['currency']
    assert payout.beneficiary_name == payload['beneficiary_name']
    assert payout.beneficiary_account == payload['beneficiary_account']
    assert payout.description == payload['description']
    assert payout.created_by == creator


def test_celery_called_process_payout(mocker, creater_client, list_create_payout_url, payload):
    mock_delay = mocker.patch('api.views.process_payout.delay')
    response = creater_client.post(list_create_payout_url, data=payload, content_type='application/json')
    assert response.status_code == 201
    mock_delay.assert_called_once()
