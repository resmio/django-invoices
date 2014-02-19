from decimal import Decimal
from datetime import date, datetime

from django import test

from invoices import create_invoice, cancel_invoice


class InvoiceTestCase(test.TestCase):	

    def test_invoice(self):
        """
        Test creating and cancelling an invoice

        """
        invoice = create_invoice(
            date.today(), date.today(), currency='EUR', country='de', items=[{
                'name': 'The fish',
                'lineItemGroups': [('standard', 'hejsa', [
                    ('line item description', Decimal(1), date.today())
                ])],
            }, {
                'name': 'Consulting',
                'lineItemGroups': [('weekend', 'davs', [
                    ('7 hours tough work', Decimal(1), date.today())
                ])]
            },
        ])
        self.assertEquals(invoice.total_amount, Decimal("2.38"))
        self.assertEquals(invoice.is_paid, False)

        # then cancel the created invoice
        cancelled_invoice = cancel_invoice(invoice)
        self.assertEquals(cancelled_invoice.total_amount, Decimal("-2.38"))

    def test_sequence_number(self):
        begins = date(2014, 1, 2)
        def create_invoice():
            return create_invoice(
                begins, date.today(), currency='EUR', country='de', items=[{
                    'name': 'The fish',
                    'lineItemGroups': [('standard', 'hejsa', [
                        ('line item description', Decimal(1), date.today())
                    ])],
                }, {
                    'name': 'Consulting',
                    'lineItemGroups': [('weekend', 'davs', [
                        ('7 hours tough work', Decimal(1), date.today())
                    ])]
                },
            ])

        invoice1 = create_invoice()

        self.assertEqual(invoice1.sequence_number, None)
        invoice1.confirmed = True
        invoice1.save()

        n0 = invoice1.sequence_number
        invoice2 = create_invoice()
        invoice3 = create_invoice()
        invoice4 = create_invoice()

        self.assertEqual(invoice1.sequence_number, None)
        invoice4.confirmed = True
        invoice4.save()
        self.assertEqual(invoice4.sequence_number, n0+1)

        invoice4.sequence_number = 123
        invoice4.save()
        self.assertEqual(invoice4.number, '2014010123')

