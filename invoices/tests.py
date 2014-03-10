from decimal import Decimal
from datetime import date, datetime

from django import test
from django.utils import timezone

from invoices import create_invoice, cancel_invoice
from invoices.signals import invoice_confirmed


class InvoiceTestCase(test.TestCase):   
    def _create_invoice(self, **kwargs):
        new_kwargs = {
            'begins': date.today(),
            'ends': date.today(),
            'currency': 'EUR',
            'country': 'de',
            'items': [{
                    'name': 'The fish',
                    'lineItemGroups': [('standard', 'hejsa', [
                        ('line item description', Decimal(1), timezone.now())
                    ])],
                }, {
                    'name': 'Consulting',
                    'lineItemGroups': [('weekend', 'davs', [
                        ('7 hours tough work', Decimal(1), timezone.now())
                    ])]
                },
            ]
        }
        new_kwargs.update(kwargs)
        return create_invoice(**new_kwargs)

    def test_invoice(self):
        """
        Test creating and cancelling an invoice

        """
        invoice = self._create_invoice()
        self.assertEquals(invoice.total_amount, Decimal("2.38"))
        self.assertEquals(invoice.is_paid, False)

        # then cancel the created invoice
        cancelled_invoice = cancel_invoice(invoice)
        self.assertEquals(cancelled_invoice.total_amount, Decimal("-2.38"))

    def test_sequence_number(self):
        begins = date(2014, 1, 2)
        def create():
            return self._create_invoice(begins=begins, confirmed=False)

        invoice1 = create()

        self.assertEquals(invoice1.sequence_number, None)
        invoice1.confirmed = True
        invoice1.save()

        n0 = invoice1.sequence_number
        invoice2 = create()
        invoice3 = create()
        invoice4 = create()

        self.assertEquals(invoice4.sequence_number, None)
        invoice4.confirmed = True
        invoice4.save()
        self.assertEquals(invoice4.sequence_number, n0+1)

        invoice4.sequence_number = 123
        invoice4.save()
        self.assertEquals(invoice4.number, '2014010123')

        # if already confirmed the sequence_number should be
        # assigned on creation
        invoice5 = self._create_invoice(confirmed=True)
        self.assertEqual(invoice5.sequence_number, n0+2)

    def test_confirmed_signal(self):
        """
        Test that the invoice_confirmed signal gets emitted correctly

        """
        # it is a dict so that it can be modified inside the function
        counter = {'n_emits': 0}
        def on_invoice_confirmed(*args, **kwargs):
            counter['n_emits'] += 1
        invoice_confirmed.connect(on_invoice_confirmed)

        invoice = self._create_invoice(confirmed = False)
        self.assertEquals(counter['n_emits'], 0)
        invoice.confirmed = True
        invoice.save()
        self.assertEquals(counter['n_emits'], 1)
        # only the first confirmation should count
        invoice.confirmed = False
        invoice.save()
        invoice.confirmed = True
        invoice.save()
        self.assertEquals(counter['n_emits'], 1)

        # invoice confirmed on creation should emit the signal too
        self._create_invoice(confirmed = True)
        self.assertEquals(counter['n_emits'], 2)

