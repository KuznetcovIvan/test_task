from rest_framework import viewsets

from payouts.models import Payout
from payouts.tasks import process_payout

from .serializers import PayoutReadSerializer, PayoutUpdateSerializer, PayoutWriteSerializer


class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.select_related('created_by').all()
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        user = self.request.user
        payouts = Payout.objects.select_related('created_by')
        if user.is_staff:
            return payouts
        return payouts.filter(created_by=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PayoutWriteSerializer
        if self.action == 'partial_update':
            return PayoutUpdateSerializer
        return PayoutReadSerializer

    def perform_create(self, serializer):
        payout = serializer.save()
        process_payout.delay(str(payout.id))
