from django.contrib import admin
from django import forms
from django.utils.translation import ugettext, ungettext, ugettext_lazy as _
from django.contrib import messages

from invoices.models import Invoice, Item, LineItem
from invoices import cancel_invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('user', 'begins', 'ends', 'is_paid')

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    readonly_fields = ('total_amount', 'confirmed')
    list_display = ('user', 'begins', 'ends', 'total_amount', 'is_paid', 'confirmed')
    list_filter = ('is_paid', 'confirmed')
    actions = ['cancel_invoices', 'confirm_invoices']

    def cancel_invoices(self, request, queryset):
        if queryset.filter(confirmed=False).count():
            message = ugettext("Unconfirmed invoices cannot be cancelled, you can just remove them")
            messages.error(request, "The message")
            return

        for invoice in queryset:
            cancel_invoice(invoice)

        message = ungettext("successfully cancelled %(count)d invoice",
            "successfully cancelled %(count)d invoices", queryset.count()) % {'count': queryset.count()}
        self.message_user(request, message)
    cancel_invoices.short_description = _('Cancel selected invoices')

    def confirm_invoices(self, request, queryset):
        count = 0
        for invoice in queryset:
            if not invoice.confirmed:
                invoice.confirmed = True
                invoice.save()
                count += 1

        message = ungettext("successfully confirmed %(count)d invoice",
            "successfully confirmed %(count)d invoices", count) % {'count': count}
        self.message_user(request, message)
    confirm_invoices.short_description = _('Confirm selected invoices')



