import datetime
from decimal import Decimal

import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from api.models import Loan, Payment, Client


class TestViews(TestCase):
    def setUp(self) -> None:
        self.new_client = Client.objects.create(name="Felicity",
                                                surname="Jones",
                                                email="felicity@gmail.com",
                                                telephone="11999661781",
                                                cpf="69495165498")

        self.loan = Loan.objects.create(client_id=self.new_client,
                                        amount=1000,
                                        term=12,
                                        rate=0.05,
                                        date=datetime.datetime(2019, 5, 9, 3, 18, tzinfo=pytz.UTC))

        self.payment = Payment.objects.create(loan_id=self.loan,
                                              payment_choice='made',
                                              date=datetime.datetime(2019, 5, 7, 4, 18, tzinfo=pytz.UTC),
                                              amount=85.6)

        self.debt_client = Client.objects.create(name="New Felicity",
                                                 surname="New Jones",
                                                 email="felicity@gmail.com",
                                                 telephone="11999661781",
                                                 cpf="69495165498")

        self.debt_loan = Loan.objects.create(client_id=self.debt_client,
                                             amount=1000,
                                             term=12,
                                             rate=0.05,
                                             date=datetime.datetime(2019, 5, 9, 3, 18, tzinfo=pytz.UTC))

        self.first_payment = Payment.objects.create(loan_id=self.debt_loan,
                                                    payment_choice='made',
                                                    date=datetime.datetime(2019, 5, 1, 4, 18, tzinfo=pytz.UTC),
                                                    amount=85.6)

        self.third_payment = Payment.objects.create(loan_id=self.debt_loan,
                                                    payment_choice='missed',
                                                    date=datetime.datetime(2019, 5, 2, 4, 18, tzinfo=pytz.UTC),
                                                    amount=85.6)

        self.second_payment = Payment.objects.create(loan_id=self.debt_loan,
                                                     payment_choice='made',
                                                     date=datetime.datetime(2019, 5, 3, 4, 18, tzinfo=pytz.UTC),
                                                     amount=85.6)

        self.client_url = reverse('api:clients')
        self.loan_url = reverse('api:loans')
        self.payment_url = reverse('api:payments', kwargs={'loan_id': self.loan.loan_id})

    def test_create_client(self):
        response = self.client.post(self.client_url,
                                    {
                                        'name': 'Nome',
                                        'surname': 'Sobrenome',
                                        'email': 'nome@gmail.com',
                                        'telephone': '6533245152',
                                        'cpf': '69495165498'
                                    })

        self.assertEqual(response.status_code, 201)

        last_client = Client.objects.last()

        last_client.refresh_from_db()
        self.assertEqual(last_client.name, 'Nome')
        self.assertEqual(last_client.surname, 'Sobrenome')
        self.assertEqual(last_client.email, 'nome@gmail.com')
        self.assertEqual(last_client.telephone, '1198453678')
        self.assertEqual(last_client.cpf, '666503264965')

    def test_create_loan(self):
        response = self.client.post(self.loan_url,
                                    {
                                        'client_id': self.new_client.client_id,
                                        'amount': 2000,
                                        'term': 12,
                                        'rate': 0.04,
                                        'date': datetime.datetime(2019, 5, 15, 8, 00, tzinfo=pytz.UTC)
                                    })

        self.assertEqual(response.status_code, 201)

        last_loan = Loan.objects.last()

        last_loan.refresh_from_db()
        self.assertEqual(last_loan.amount, 2000)
        self.assertEqual(last_loan.term, 12)
        self.assertEqual(last_loan.rate, Decimal('0.02'))
        self.assertEqual(last_loan.date, datetime.datetime(2019, 5, 15, 8, 00, tzinfo=pytz.UTC))

    def test_create_loan_debt(self):
        response = self.client.post(self.loan_url,
                                    {
                                        'client_id': self.debt_client.client_id,
                                        'amount': 2000,
                                        'term': 12,
                                        'rate': 0.04,
                                        'date': datetime.datetime(2019, 5, 15, 8, 00, tzinfo=pytz.UTC)
                                    })

        self.assertEqual(response.status_code, 201)

        last_loan = Loan.objects.last()

        last_loan.refresh_from_db()
        self.assertEqual(last_loan.amount, 2000)
        self.assertEqual(last_loan.term, 12)
        self.assertEqual(last_loan.rate, Decimal('0.08'))
        self.assertEqual(last_loan.date, datetime.datetime(2019, 5, 15, 8, 00, tzinfo=pytz.UTC))

    def test_create_loan_four_month_debt(self):
        Payment.objects.create(loan_id=self.debt_loan,
                               payment_choice='missed',
                               date=datetime.datetime(2019, 7, 2, 6, 18, tzinfo=pytz.UTC),
                               amount=85.6)
                               
        Payment.objects.create(loan_id=self.debt_loan,
                               payment_choice='missed',
                               date=datetime.datetime(2019, 8, 2, 7, 18, tzinfo=pytz.UTC),
                               amount=85.6)
        Payment.objects.create(loan_id=self.debt_loan,
                               payment_choice='missed',
                               date=datetime.datetime(2019, 9, 2, 8, 18, tzinfo=pytz.UTC),
                               amount=85.6)
        response = self.client.post(self.loan_url,
                                    {
                                        'client_id': self.debt_client.client_id,
                                        'amount': 2000,
                                        'term': 12,
                                        'rate': 0.04,
                                        'date': datetime.datetime(2019, 5, 15, 8, 00, tzinfo=pytz.UTC)
                                    })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0],
                         ErrorDetail(string='O cliente não pagou 3 ou mais faturas.', code='invalid'))