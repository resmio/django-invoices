from decimal import Decimal

from datetime import date, datetime

from django import test

from invoices import create_invoice

class InvoiceTestCase(test.TestCase):	

    def test_create_invoice(self):
        """
        Test creating an invoice

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
