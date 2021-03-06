# Generated by Django 4.0.3 on 2022-05-11 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='nom et prénom')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='nom utilisateur')),
                ('user_api', models.BooleanField(default=False, verbose_name="utilisateur d'api")),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='email')),
                ('image', models.ImageField(blank=True, default='profiles/user.png', null=True, upload_to='profiles/', verbose_name='photo de profil')),
                ('slug', models.CharField(default=uuid.uuid4, editable=False, max_length=255, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='utilisateur')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Fiche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='nom')),
                ('last_name', models.CharField(max_length=255, verbose_name='prénom')),
                ('contact_one', models.CharField(max_length=10, verbose_name='contact 1')),
                ('contact_two', models.CharField(blank=True, max_length=10, null=True, verbose_name='contact 2')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('birth', models.DateField(verbose_name='date de naissance')),
                ('birth_place', models.CharField(blank=True, max_length=255, null=True, verbose_name='lieu de naissance')),
                ('identity', models.CharField(blank=True, choices=[('CNI', 'cni'), ('PASSPORT', 'passport'), ('ATTESTATION', 'attestation'), ('CARTE_CONSULAIRE', 'carte_consulaire')], default='CNI', max_length=50, null=True, verbose_name="pièce d'identité")),
                ('identity_num', models.CharField(blank=True, max_length=255, null=True, verbose_name="numéro de pièce d'identité")),
                ('identity_card_recto', models.ImageField(blank=True, default='clients/identity/empty.jpg', null=True, upload_to='clients/identity/', verbose_name="pièce d'identité recto")),
                ('identity_card_verso', models.ImageField(blank=True, default='clients/identity/empty.jpg', null=True, upload_to='clients/identity/', verbose_name="pièce d'identité verso")),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Pays')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='ville')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='adresse')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to='user.profile', verbose_name='créateur')),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='owner', to='user.profile', verbose_name='client')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
    ]
