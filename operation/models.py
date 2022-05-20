import uuid
from django.db import models

from carte.models import Carte, TypeCarte
from payment.models import Payment
from user.models import Profile, Fiche

# Create your models here.
class TypeOperation(models.Model):
    name = models.CharField(max_length=50, verbose_name="nom")
    slug = models.SlugField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.name}'

class FraisOperation(models.Model):

    operation_type = models.ForeignKey(TypeOperation, on_delete=models.CASCADE, verbose_name="type d'operation")
    carte_type = models.ForeignKey(TypeCarte, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="type de carte")

    AMOUNT = 'montant'
    PERCENTAGE = 'pourcentage'
    recharge_fee_choices = [
        (AMOUNT, 'Montant'),
        (PERCENTAGE, 'Pourcentage')
    ]
    recharge_fee = models.CharField(
        max_length=15,
        choices=recharge_fee_choices,
        default=AMOUNT,
        verbose_name="Frais d'operation"
    )
    buy_carte_amount = models.FloatField(null=True, blank=True, verbose_name="Montant à l'achat de la carte")
    initial_amount_value = models.FloatField(null=True, blank=True, verbose_name="montant initial")
    final_amount_value = models.FloatField(null=True, blank=True, verbose_name="montant final")
    amount_value = models.FloatField(null=True, blank=True, verbose_name="montant frais")
    percentage_value = models.FloatField(null=True, blank=True, verbose_name="valeur du pourcentage")
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    date_addee = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('operation_type',)
    
    def __str__(self):

        if self.carte_type:
            return f'{self.operation_type.name} - {self.carte_type.name.upper()} - {self.recharge_fee.upper()}'

        return f'{self.operation_type.name} - {self.recharge_fee.upper()}'



class Operation(models.Model):
    STATUS_ATTENTE = 'ATTENTE'
    STATUS_ACCEPTE = 'ACCEPTE'
    STATUS_VALIDE = 'VALIDE'
    STATUS_REFUSE = 'REFUSE'
    STATUS_ANNULE = 'ANNULE'
    status_recharge_choices = [
        (STATUS_ATTENTE, 'En Attente'),
        (STATUS_ACCEPTE, 'Accepté'),
        (STATUS_VALIDE, 'Validé'),
        (STATUS_REFUSE, 'Refusé'),
        (STATUS_ANNULE, 'Annulé'),
    ]
    
    status_operation = models.CharField(
        max_length=15,
        choices=status_recharge_choices,
        default=STATUS_ATTENTE,
    )

    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True, blank=True)

    operation_type = models.ForeignKey(TypeOperation, on_delete=models.DO_NOTHING)

    client = models.ForeignKey(Fiche, on_delete=models.DO_NOTHING, null=True, blank=True) #client
    
    operator = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, blank=True) #operatuer traitant

    carte = models.ForeignKey(Carte, on_delete=models.DO_NOTHING) # carte

    montant_initial = models.BigIntegerField(null=True, blank=True)
    frais_operation = models.CharField(max_length=20, null=True, blank=True)
    montant_operation = models.BigIntegerField(null=True, blank=True)

    identifiant = models.UUIDField(default= uuid.uuid4, editable=False)
    date_demande = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    date_acceptation = models.DateTimeField( null=True, blank=True)
    date_validation = models.DateTimeField( null=True, blank=True)
    date_annulation = models.DateTimeField( null=True, blank=True)
    slug = models.SlugField(default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return f"{self.identifiant}"

