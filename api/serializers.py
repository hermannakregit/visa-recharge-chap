from rest_framework import serializers

from operation.models import Operation, TypeOperation, FraisOperation
from carte.models import Carte, TypeCarte
from user.models import Fiche
from payment.models import Payment

class FraisOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraisOperation
        fields = '__all__'

class TypeOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOperation
        fields = '__all__'


class TypeCarteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCarte
        fields = ['name', 'logo', 'rechargement_url', 'plafond']

class CarteSerializer(serializers.ModelSerializer):
    type_carte = TypeCarteSerializer(many=False)
    class Meta:
        model = Carte
        fields = [
            'type_carte',
            "carte_client_id",
            "carte_num",
            "carte_exp_month",
            "carte_exp_year",
            "slug",
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['confirmed']


class OperationSerializer(serializers.ModelSerializer):
    carte = CarteSerializer(many=False)
    payment = PaymentSerializer(many=False)
    class Meta:
        model = Operation
        fields = [
            "payment",
            "carte",
            "status_operation",
            "frais_operation",
            "montant_operation",
            "identifiant",
            "slug",
            "date_added",
        ]

class FicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiche
        fields = [
            "first_name",
            "last_name",
            "contact_one",
            "contact_two",
            "email",
            "birth",
            "birth_place",
            "identity",
            "identity_num",
            "country",
            "city",
            "address",
            "slug",
        ]