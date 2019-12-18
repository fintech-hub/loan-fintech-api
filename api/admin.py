from django.contrib import admin
from .models import Loan, Client, Payment


class LoanAdmin(admin.ModelAdmin):
    list_display = [
        'loan_id',
        'amount',
        'term',
        'rate',
        'date'
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'client_id',
        'name',
        'surname',
        'email',
        'telephone',
        'cpf',
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "loan_id",
        "payment_choice",
        "date",
        "amount"
    )


admin.site.register(Loan, LoanAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Payment, PaymentAdmin)
