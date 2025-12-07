from django.db import models
from django.utils.translation import gettext_lazy as _


class PURCHASEDSTATUS(
    models.TextChoices
):
    PENDING = 'P' , _("pending")
    PROCESSING = 'PR' , _("processing")
    DELIVERED = 'D' , _("delivered")
    CANCELLED = 'C' , _("cancelled")
     