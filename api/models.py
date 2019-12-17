import decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext as _
from datetime import datetime, timezone
from django.core.validators import MinValueValidator
from .validators import validate_cpf, validate_phone


class CommonClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(CommonClass):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=100)
    surname = models.CharField(_('Surname'), max_length=100)
    email = models.EmailField(_('Email'), max_length=254)
    telephone = models.CharField(_('Telephone'), max_length=11, validators=[validate_phone])
    cpf = models.CharField(_('CPF'), max_length=11, validators=[validate_cpf], unique=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'Client Id: {self.client_id}'


class Loan(CommonClass):
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    loan_id = models.AutoField(primary_key=True, unique=True)
    amount = models.DecimalField(_('Amount'), max_digits=15, decimal_places=2)
    term = models.IntegerField(_('Term'), validators=[MinValueValidator(1)])
    rate = models.DecimalField(_('Rate'), max_digits=5, decimal_places=2)
    date = models.DateTimeField(_('Date'), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f'Loan Id: {self.loan_id} instalment: {self.instalment}'

    @property
    def balance(self, date=datetime.now().astimezone(tz=timezone.utc)):
        credit = len(self.payment_set.filter(payment='made', date__lte=date))
        if (credit == 0):
            return self.instalment * self.term
        else:
            return self.instalment * (self.term - credit)

    @property
    def instalment(self):
        r = self.rate / self.term
        instalment = (r + (r / ((1 + r) ** self.term - 1))) * self.amount
        # Truncated value for 0.00 format, without round
        return decimal.Decimal(instalment).quantize(
            decimal.Decimal((0, (1,), -2)), rounding=decimal.ROUND_DOWN
        )


class Payment(CommonClass):

    PAYMENT_CHOICES = (('made', 'made'), ('missed', 'missed'))

    loan_id = models.ForeignKey(_('Loan'), on_delete=models.CASCADE)
    payment_choice = models.CharField(_('Payment'), max_length=6, choices=PAYMENT_CHOICES)
    date = models.DateTimeField(_('Date'), auto_now=False, auto_now_add=False)
    amount = models.DecimalField(_('Amount'), max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment (loan_id={self.loan_id}, payment_choice={self.payment_choice}, date={self.date}, amount={self.amount})"
