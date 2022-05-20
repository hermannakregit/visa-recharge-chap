# Generated by Django 4.0.3 on 2022-05-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0004_alter_typecarte_buy_alter_typecarte_recharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='typecarte',
            name='initial',
            field=models.BigIntegerField(blank=True, default=2000, null=True, verbose_name='montant initial'),
        ),
        migrations.AlterField(
            model_name='typecarte',
            name='plafond',
            field=models.BigIntegerField(blank=True, default=10000000, null=True, verbose_name='plafond'),
        ),
    ]
