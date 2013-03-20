from django.contrib import admin
from django import forms
from django.utils.translation import ugettext, ungettext, ugettext_lazy as _

from invoices.models import Invoice, Item, LineItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('user', 'begins', 'ends', 'is_paid')

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    readonly_fields = ('total_amount',)
    list_display = ('user', 'begins', 'ends', 'total_amount', 'is_paid')
    list_filter = ('is_paid',)
    actions = ['cancel_invoices']

    def cancel_invoices(self, request, queryset):

        for invoice in queryset:
            cancelled_invoice = Invoice.objects.create(
                cancels=invoice,
                user=invoice.user,
                begins=invoice.begins,
                ends=invoice.ends,
                due_date=invoice.due_date,
                is_paid=invoice.is_paid,
                currency=invoice.currency,
                name=invoice.name,
                company=invoice.company,
                address1=invoice.address1,
                address2=invoice.address2,
                city=invoice.city,
                zip_code=invoice.zip_code,
                country=invoice.country
            )

            # this will update total amounts on the invoice
            cancelled_invoice.calculate()

        message = ungettext("successfully cancelled %(count)d invoice",
            "successfully cancelled %(count)d invoices", queryset.count()) % {'count': queryset.count()}
        self.message_user(request, message)
    cancel_invoices.short_description = _('Cancel selected invoices')

