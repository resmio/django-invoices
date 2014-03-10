from django.dispatch import Signal

invoice_ready = Signal(providing_args=["invoice"])
invoice_confirmed = Signal(providing_args=["invoice"])