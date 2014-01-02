from __future__ import division
from decimal import Decimal

from django.db import models, transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse

from invoices.signals import invoice_ready

class Invoice(models.Model):
    """
    Invoice

    """
    user = models.ForeignKey(User, blank=True, null=True, related_name='invoices')
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)
    begins = models.DateField(verbose_name=_('Begin'))
    ends = models.DateField(verbose_name=_('End'))
    due_date = models.DateField(verbose_name=_('Due date'), null=True, blank=True)
    is_paid = models.BooleanField(verbose_name=_('Is paid'), default=False)
    currency = models.CharField(max_length=3, default='EUR')
    name = models.CharField(max_length=512, verbose_name=_('Name'), blank=True)
    company = models.CharField(max_length=512, verbose_name=_('Company'), blank=True)
    address1 = models.CharField(max_length=512, verbose_name=_('Address 1'), blank=True)
    address2 = models.CharField(max_length=512, verbose_name=_('Address 2'), blank=True)
    city = models.CharField(max_length=256, verbose_name=_('City'), blank=True)
    zip_code = models.CharField(max_length=128, verbose_name=_('Zip code'), blank=True)
    country = models.CharField(max_length=2, verbose_name=_('Country'), blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"), help_text=_('Without VAT'))
    credit = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Credit'), default=Decimal("0.0"), help_text=_("Add credit"))
    credit_reason = models.TextField(verbose_name="Reason for credit", blank=True)
    vat_amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"))
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"), help_text=_('Including VAT'))
    vat = models.PositiveIntegerField(verbose_name=_('VAT'), default=19)
    cancels = models.OneToOneField("Invoice", blank=True, null=True)

    @property
    def number(self):
        """
        Invoice number of format "YYYYMM0001"

        """
        return '%d%s%s' % (self.begins.year, unicode(self.begins.month).zfill(2), unicode(self.pk).zfill(4))

    def calculate(self, silent=False):

        with transaction.atomic():
            if self.cancels:
                # cancellation of existing invoice
                for item in self.cancels.items.all():
                    i = Item.objects.create(invoice=self, name=item.name, total_amount = -item.total_amount)
                    self.amount += i.total_amount
                    for item_group in item.line_item_groups.all():
                        LineItemGroup.objects.create(item=i, item_type=item_group.item_type, amount=-item_group.amount, description=item_group.description)
                self.amount += self.credit

                # for cancelleations set both invoices to status paid
                self.cancels.is_paid = True
                self.cancels.save()
                self.is_paid = True
            else:
                # regular invoice
                for item in self.items.all():
                    for item_group in item.line_item_groups.all():
                        item_group.amount = item_group.line_items.aggregate(Sum('amount'))['amount__sum'] or Decimal("0.0")
                        item_group.save()
                    item.total_amount = item.line_item_groups.aggregate(Sum('amount'))['amount__sum'] or Decimal("0.0")
                    item.save()
                    self.amount += item.total_amount
                self.amount -= self.credit

            # add vat
            self.vat_amount = self.amount * Decimal(self.vat / 100).quantize(Decimal('1.00'))
            self.total_amount = self.amount + self.vat_amount
            self.save()
            transaction.commit()

        if not silent:
            invoice_ready.send(sender=self, invoice=self)
        return self

    def get_absolute_url(self):
        return reverse('invoice_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s, %s - %s" % (self.user, self.begins, self.ends)

    class Meta:
        ordering = ['-begins', '-ends',]

class Item(models.Model):
    """
    Item

    """
    invoice = models.ForeignKey(Invoice, related_name='items')
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    total_amount = models.DecimalField(max_digits=7,
        decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"))

    def __unicode__(self):
        return u'%s' % self.name

class LineItemType(models.Model):
    """
    Line item type

    """
    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        return u'%s' % self.identifier

class LineItemGroup(models.Model):
    """
    Line item group

    """
    item = models.ForeignKey(Item, related_name='line_item_groups')
    item_type = models.ForeignKey(LineItemType, related_name='line_item_groups')
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'), default=Decimal("0.0"))
    description = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.item, self.item_type)

class LineItem(models.Model):
    """
    Line item

    """
    item = models.ForeignKey(Item, related_name='line_items')
    item_group = models.ForeignKey(LineItemGroup, related_name='line_items', null=True)
    description = models.CharField(max_length=512, verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Amount'))
    date = models.DateTimeField(verbose_name=_('Date'))

    def __unicode__(self):
        return self.description
