from django.dispatch import Signal

invoice_ready = Signal(providing_args=["invoice"])