from django.contrib import admin
from django import forms
from django.utils.translation import ugettext, ungettext, ugettext_lazy as _

from invoices.models import Invoice, Item, LineItem
from invoices import cancel_invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('user', 'begins', 'ends', 'is_paid')

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    readonly_fields = ('total_amount',)
    list_display = ('user', 'begins', 'ends', 'total_amount', 'is_paid', 'confirmed')
    list_filter = ('is_paid', 'confirmed')
    actions = ['cancel_invoices']

    def cancel_invoices(self, request, queryset):

        for invoice in queryset:
            cancel_invoice(invoice)

        message = ungettext("successfully cancelled %(count)d invoice",
            "successfully cancelled %(count)d invoices", queryset.count()) % {'count': queryset.count()}
        self.message_user(request, message)
    cancel_invoices.short_description = _('Cancel selected invoices')

