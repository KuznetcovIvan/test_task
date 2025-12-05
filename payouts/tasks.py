from random import choice
from time import sleep

from celery import shared_task

from payouts.models import Payout, PayoutStatus

MESSAGE_SKIP = 'Payout {} skipped'
MESSAGE_COMPLETED = 'Payout {} completed as {}'


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3, default_retry_delay=60)
def process_payout(payout_id: str) -> str:
    updated = Payout.objects.filter(
        id=payout_id,
        status__in=[PayoutStatus.NEW, PayoutStatus.PROCESSING],
    ).update(status=PayoutStatus.PROCESSING)
    if not updated:
        return MESSAGE_SKIP.format(payout_id)

    sleep(10)
    # Имитация i/o к сервису банка с передачей payout_id как idempotency_key.
    # Банк гарантирует что платёж выполнится только один раз и вернёт результат первого вызова.
    result = choice([PayoutStatus.COMPLETED, PayoutStatus.FAILED])

    updated = Payout.objects.filter(id=payout_id, status=PayoutStatus.PROCESSING).update(status=result)
    return MESSAGE_SKIP.format(payout_id) if not updated else MESSAGE_COMPLETED.format(payout_id, result)
