from django import forms
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext, ngettext, gettext_lazy as _

from invoices import cancel_invoice
from invoices.models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('user', 'begins', 'ends', 'is_paid', 'status',
                  'payment_reminder_date', 'dunning_1_date', 'dunning_2_date',
                  'collection')


class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    readonly_fields = ('total_amount', 'confirmed')
    list_display = ('user', 'begins', 'ends', 'total_amount', 'is_paid',
                    'confirmed')
    list_filter = ('is_paid', 'confirmed')
    actions = ['cancel_invoices', 'confirm_invoices', 'delete_invoices']
    search_fields = ['owner__pk', 'owner__name']

    def cancel_invoices(self, request, queryset):
        if queryset.filter(confirmed=False).count():
            message = gettext('Unconfirmed invoices cannot be cancelled, '
                               'you can just delete them')
            messages.error(request, message)
            return

        for invoice in queryset:
            cancel_invoice(invoice)

        message = ngettext(
            'successfully cancelled %(count)d invoice',
            'successfully cancelled %(count)d invoices',
            queryset.count()) % {'count': queryset.count()}
        self.message_user(request, message)
    cancel_invoices.short_description = _('Cancel selected invoices')

    def confirm_invoices(self, request, queryset):
        count = 0
        for invoice in queryset:
            if not invoice.confirmed:
                invoice.confirmed = True
                invoice.save()
                count += 1

        message = ngettext(
            'successfully confirmed %(count)d invoice',
            'successfully confirmed %(count)d invoices',
            count) % {'count': count}
        self.message_user(request, message)
    confirm_invoices.short_description = _('Confirm selected invoices')

    def delete_invoices(self, request, queryset):
        if queryset.filter(confirmed=True).count():
            message = gettext(
                'You cannot delete confirmed invoices, '
                'create a cancellation instead')
            messages.error(request, message)
            return
        count = 0

        count = queryset.count()
        queryset.delete()
        message = ngettext(
            'successfully deleted %(count)d invoice',
            'successfully deleted %(count)d invoices',
            count) % {'count': count}
        self.message_user(request, message)
    delete_invoices.short_description = _('Delete unconfirmed invoices')
