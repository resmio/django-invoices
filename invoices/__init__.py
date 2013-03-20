from invoices.models import Invoice, Item, LineItemType, LineItemGroup, LineItem

def create_invoice(begins=None, ends=None, currency='EUR', due_date=None, is_paid=False, name='', company='',
    address1='', address2='', city='', zip_code='', country='', vat=19, items=[], user=None):
    """
    Create a new invoice

    """
    invoice = Invoice.objects.create(begins=begins, ends=ends, currency=currency, due_date=due_date, 
        is_paid=is_paid, name=name, company=company, address1=address1, address2=address2, city=city,
            zip_code=zip_code, country=country, vat=vat, user=user)

    for item in items:
        i = Item.objects.create(invoice=invoice, name=item.get('name', ''))
        for item_type, description, line_items in item['lineItemGroups']:
	        line_item_type, created = LineItemType.objects.get_or_create(identifier=item_type)
	        line_item_group = LineItemGroup.objects.create(item=i, item_type=line_item_type, description=description)
	        for description, amount, date in line_items:
	            LineItem.objects.create(item=i, item_group=line_item_group, description=description, amount=amount, date=date)

    invoice.calculate()
    return invoice
