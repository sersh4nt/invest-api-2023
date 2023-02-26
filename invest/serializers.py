from rest_framework import serializers

from .models import Account, Subaccount


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class SubaccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subaccount
        fields = "__all__"
