import uuid
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="utilisateur")
    name = models.CharField(verbose_name="nom et prénom", max_length=255, blank=True, null=True)
    username = models.CharField(verbose_name="nom utilisateur",max_length=255, blank=True, null=True)
    user_api = models.BooleanField(verbose_name="utilisateur d'api", default=False)  #default 3e935bdd
    email = models.EmailField(verbose_name="email", max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name="photo de profil", null=True, blank=True, upload_to="profiles/", default="profiles/user.png")
    slug = models.CharField(max_length=255 ,default=uuid.uuid4, unique=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return f'{self.username}'


class Fiche(models.Model):

    # class fiche client

    CNI = 'CNI'
    PASSPORT = 'PASSPORT'
    ATTESTATION = 'ATTESTATION'
    CARTE_CONSULAIRE = 'CARTE_CONSULAIRE'
    CHOIX_PIECE = [
        (CNI, 'cni'),
        (PASSPORT, 'passport'),
        (ATTESTATION, 'attestation'),
        (CARTE_CONSULAIRE, 'carte_consulaire')
    ]

    owner = models.OneToOneField(
        Profile,
        on_delete=models.DO_NOTHING,
        null=True, blank=True,
        verbose_name="client",
        related_name="owner"
    )
    creator = models.ForeignKey(Profile, related_name="creator", null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="créateur")
    first_name = models.CharField(max_length=255, verbose_name="nom")
    last_name = models.CharField(max_length=255, verbose_name="prénom")
    contact_one = models.CharField(max_length=10, verbose_name="contact 1")
    contact_two = models.CharField(max_length=10, null=True, blank=True, verbose_name="contact 2")
    email = models.EmailField(verbose_name="email")
    birth = models.DateField(verbose_name="date de naissance")
    birth_place = models.CharField(max_length=255, null=True, blank=True, verbose_name="lieu de naissance")
    identity = models.CharField(max_length=50, choices=CHOIX_PIECE, default=CNI, verbose_name="pièce d'identité", null=True, blank=True)
    identity_num = models.CharField(max_length=255, verbose_name="numéro de pièce d'identité", null=True, blank=True)
    identity_card_recto = models.ImageField(upload_to='clients/identity/', default="clients/identity/empty.jpg", blank=True, null=True, verbose_name="pièce d'identité recto")
    identity_card_verso = models.ImageField(upload_to='clients/identity/', default="clients/identity/empty.jpg", blank=True, null=True, verbose_name="pièce d'identité verso")
    country = CountryField(blank_label='(Sélectionner votre pays)', verbose_name="Pays")
    city = models.CharField(max_length=255, verbose_name="ville", null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="adresse")
    slug = models.SlugField(max_length=200, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
