from decimal import Decimal


def create_invoice(begins=None, ends=None, currency='EUR', due_date=None,
                   is_paid=False, name='', company='', address1='',
                   address2='', city='', zip_code='', country='', vat=19,
                   credit=Decimal('0.0'), credit_reason=None, items=[],
                   user=None, confirmed=True):
    """
    Create a new invoice

    """
    from invoices.models import Invoice, Item, LineItemType, LineItemGroup, \
        LineItem

    invoice = Invoice.objects.create(
        begins=begins, ends=ends, currency=currency, due_date=due_date,
        is_paid=is_paid, name=name, company=company, address1=address1,
        address2=address2, city=city, zip_code=zip_code, country=country,
        vat=vat, credit=credit, credit_reason=credit_reason or '',
        user=user, confirmed=confirmed)

    for item in items:
        i = Item.objects.create(invoice=invoice, name=item.get('name', ''))
        for item_type, description, line_items in item['lineItemGroups']:
            line_item_type, created = LineItemType.objects.get_or_create(
                identifier=item_type)
            line_item_group = LineItemGroup.objects.create(
                item=i, item_type=line_item_type, description=description)
            for description, amount, date in line_items:
                LineItem.objects.create(item=i, item_group=line_item_group,
                                        description=description, amount=amount,
                                        date=date)

    return invoice.calculate()


def cancel_invoice(invoice):
    """
    Cancel an invoice by creating a credit nota (a new invoice with the
    negative amount)

    """
    from invoices.models import Invoice

    cancelled_invoice = Invoice.objects.create(
        cancels=invoice,
        owner=invoice.owner,
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
        country=invoice.country,
        confirmed=invoice.confirmed,
        vat=invoice.vat
    )
    return cancelled_invoice.calculate()
