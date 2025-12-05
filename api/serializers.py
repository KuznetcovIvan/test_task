from rest_framework import serializers

from payouts.models import Payout


class PayoutBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['amount', 'currency', 'beneficiary_name', 'beneficiary_account', 'description']


class PayoutReadSerializer(PayoutBaseSerializer):
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Payout
        fields = ['id', *PayoutBaseSerializer.Meta.fields, 'status', 'created_at', 'updated_at', 'created_by']


class PayoutWriteSerializer(PayoutBaseSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        return PayoutReadSerializer(instance, context=self.context).data


class PayoutUpdateSerializer(PayoutReadSerializer):
    class Meta(PayoutReadSerializer.Meta):
        read_only_fields = [field for field in PayoutReadSerializer.Meta.fields if field != 'status']
