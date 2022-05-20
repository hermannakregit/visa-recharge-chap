import uuid
from django.db import models

from user.models import Profile, Fiche
from carte.models import Carte

# Create your models here.

# Payment type
# Carte = use slug
# Opération = use slug
#

# Create your models here.
class Payment(models.Model):
    carte = models.ForeignKey(Carte, null=True, blank=True, on_delete=models.CASCADE)
    initiator = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    client =  models.ForeignKey(Fiche, on_delete=models.DO_NOTHING)

    code = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=50, null=True, blank=True)
    montant = models.BigIntegerField()
    cash = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    metadata = models.TextField(null=True, blank=True)
    transaction_id = models.SlugField(default=uuid.uuid4, editable=False)
    operator_id = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    api_response_id = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.transaction_id


class Avoir(models.Model):
    paiement = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE
    )
    montant = models.CharField(max_length=50)
    date_remboursement = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)