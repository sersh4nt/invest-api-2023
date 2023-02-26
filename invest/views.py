from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import Account
from . import tinkoff
from .serializers import AccountSerializer, SubaccountSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []

    @action(detail=True, methods=["POST"])
    def retrieve_subaccounts(self, request, pk=None):
        account = self.get_object()
        subaccounts = tinkoff.get_subaccounts(account.token)
        serializer = SubaccountSerializer(subaccounts, many=True)
        return Response(serializer.data)
