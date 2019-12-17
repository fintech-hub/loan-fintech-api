from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .models import Client, Loan, Payment
from .serializers import ClientSerializer, PaymentSerializer, LoanSerializer, BalanceSerializer


class ClientCreateView(CreateAPIView):
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientView(RetrieveAPIView):
    serializer_class = ClientSerializer

    def get(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, client_id=client_id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class LoanCreateView(CreateAPIView):
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PaymentCreateView(CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, loan_id, *args, **kwargs):
        # loan = get_object_or_404(Loan, loan_id=loan_id)
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BalanceView(RetrieveAPIView):
    serializer_class = BalanceSerializer

    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(Loan, loan_id=loan_id)
        serializer = BalanceSerializer(loan)
        return Response(serializer.data)


def test(request):
    return HttpResponse("Loan Fintech API")
