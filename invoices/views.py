from django.views.generic import ListView, DetailView

from invoices.models import Invoice

class InvoiceListView(ListView):
    model = Invoice
    context_object_name = 'invoice_list'

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user, confirmed=True)

class InvoiceDetailView(DetailView):
    model = Invoice
    context_object_name = 'invoice'

    def get_queryset(self):
    	qs = Invoice.objects.all()
    	if not self.request.user.is_staff:
    		qs = qs.filter(user=self.request.user)
        return qs
