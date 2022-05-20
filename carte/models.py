import datetime
import uuid
from django.db import models

from user.models import Profile, Fiche

# Create your models here.

class TypeCarte(models.Model):
    DEFAULT_URL = f'https://www.gtpportal.com/Visa/MerchantLite/UserLogin.aspx?ReturnUrl=%2fVisa%2fMerchantLite'

    name = models.CharField(verbose_name="nom", max_length=50)
    logo = models.ImageField(verbose_name="logo", upload_to='types_cartes/', blank=True, null=True)
    rechargement_url = models.URLField(verbose_name="lien de rechergement" ,default=DEFAULT_URL)
    initial = models.BigIntegerField(verbose_name="montant initial", default=2000, null=True, blank=True)
    plafond = models.BigIntegerField(verbose_name="plafond", default=10000000, null=True, blank=True)
    buy =models.BooleanField(verbose_name="achat", default=False)
    recharge =models.BooleanField(verbose_name="recharge", default=False)
    slug = models.SlugField(default=uuid.uuid4, unique=True, editable=False)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name



class Carte(models.Model):
    owner = models.ForeignKey(Fiche, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="propriétaire")
    creator = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Créateur")
    type_carte = models.ForeignKey(
        TypeCarte,
        on_delete=models.DO_NOTHING,
        verbose_name="Type de carte"
    )

    status = models.BooleanField(verbose_name="Status", default=False)

    YEAR_CHOICES = []
    for r in range(datetime.datetime.now().year, (datetime.datetime.now().year + 20)):
        YEAR_CHOICES.append((r, r))

    MONTH_CHOICES = []
    for r in range(1, 13):
        if r<10 :
            MONTH_CHOICES.append((r, f'{"0"}{r}'))
        else:
            MONTH_CHOICES.append((r, r))

    carte_client_id = models.CharField(verbose_name="identifiant client", max_length=11, unique=True)
    carte_num = models.CharField(verbose_name="numéro de carte", max_length=18, unique=True)
    carte_exp_month = models.IntegerField(verbose_name="mois d'expiration", choices=MONTH_CHOICES, default=1)
    carte_exp_year = models.IntegerField( verbose_name="année d'expiration", choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    slug = models.SlugField(default=uuid.uuid4, unique=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return f'{self.carte_client_id}'
