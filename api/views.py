from cinetpay_sdk.s_d_k import Cinetpay
from payment.models import Payment
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User

from operation.utils import calculWithFrais

from api.serializers import CarteSerializer, OperationSerializer, FicheSerializer

from operation.models import FraisOperation, Operation, TypeOperation
from user.models import Fiche, Profile

from carte.models import Carte

from user.utils import message


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def user(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = User()
    user.username = username.lower()
    user.set_password(password)
    user.save()

    return Response({
        'message': 'success',
        'statut': '200',
    })


@api_view(['GET', 'POST'])
def userFiche(request):

    if request.method == 'POST':

        firstname = request.data.get('firstname')
        lastname= request.data.get('lastname')
        email= request.data.get('email')
        contact= request.data.get('contact')
        contactTwo= request.data.get('contactTwo')
        
        birth = request.data.get('birth')[0:10]
        #print(birth)

        birthPlace= request.data.get('birthPlace')
        identity = request.data.get('identity')
        numIdentity= request.data.get('numIdentity')
        country= request.data.get('country')
        city = request.data.get('city')
        address = request.data.get('address')

        try:

            user = User.objects.get(id = request.user.id)
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            profile = Profile.objects.get(user=user)
            profile.name = f'{firstname} {lastname}'
            profile.username = user.username
            profile.email = user.email
            profile.save()

            fiche = Fiche.objects.get_or_create(
                owner = profile,
                creator = profile,
                first_name = firstname,
                last_name = lastname,
                contact_one = contact,
                contact_two = contactTwo,
                email = email,
                birth = birth,
                birth_place = birthPlace,
                identity = identity,
                identity_num = numIdentity,
                country = country,
                city = city,
                address = address,
            )

            message(f"Bonjour M/Mme {lastname} {firstname}, votre inscription a été éffectuée avec succès, merci pour votre confiance.", contact)

            return Response({'fiche': True})

        except :
           return Response({'fiche': False})

    try:
        fiche = Fiche.objects.get(owner=request.user.profile)
        return Response({'fiche': True})
    except Fiche.DoesNotExist:
        return Response({'fiche': False})

    serializer = FicheSerializer(fiche, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserOperations(request):
    fiche = Fiche.objects.get(owner=request.user.profile)
    operations = Operation.objects.filter(client=fiche, payment__confirmed=True).exclude(payment=None)
    serializer = OperationSerializer(operations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserOperation(request, slug):

    fiche = Fiche.objects.get(owner=request.user.profile)
    
    try:
        operation = Operation.objects.get(client=fiche, slug=slug)
        serializer = OperationSerializer(operation, many=False)

        response = {
            'operation' : serializer.data,
            'frais': operation.frais_operation,
        }

        return Response(response)
    except Operation.DoesNotExist:
        return Response({
            'message': 'operation does not exist',
            'statut': 'failed',
        })


@api_view(['GET'])
def getUserCartes(request):
    fiche = Fiche.objects.get(owner=request.user.profile)
    cartes = Carte.objects.filter(owner=fiche)
    serializer = CarteSerializer(cartes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserCarte(request, slug):
    
    fiche = Fiche.objects.get(owner=request.user.profile)

    try:
        carte = Carte.objects.get(owner=fiche, slug=slug)
        serializer = CarteSerializer(carte, many=False)

        return Response(serializer.data)
    except Carte.DoesNotExist:
        return Response({
            'message': 'carte does not exist',
            'statut': 'failed',
        })


@api_view(['GET'])
def getAllCarte(request):
    cartes = Carte.objects.filter(owner=None, type_carte__buy=True)
    serializer = CarteSerializer(cartes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def calculFrais(request):

    fiche = Fiche.objects.get(owner=request.user.profile)

    montant = request.data.get('montant')

    #print('data :', request.data)

    try:

        carte = Carte.objects.get(owner=fiche, slug=request.data.get('carte'), type_carte__recharge=True)

        if not montant:
            montant = 0
        
        frai, montantTotal, service = calculWithFrais(int(montant), carte.type_carte)
        
        response = {
            'payment_amount': montantTotal,
        }

        return Response(response)

    except Carte.DoesNotExist:
        return Response({
            'message': 'carte does not exist',
            'statut': 'failed',
        })


@api_view(['POST'])
def setPayment(request):

    url = None
    frais = None
    description = None
    _montant = None

    if request.method == 'POST':

        #print(request.data)

        type_operation = TypeOperation.objects.get(name=request.data.get('type'))
        carte = Carte.objects.get(slug=request.data.get('carte'))
        fiche = Fiche.objects.get(owner=request.user.profile)

        if request.data.get('type') == 'ACHAT DE CARTE':
            frais_op = FraisOperation.objects.get(operation_type = type_operation, carte_type=carte.type_carte)
            _montant = frais_op.buy_carte_amount
            
            description = f"Achat de carte la carte {carte.carte_client_id} pour M/mme {fiche.last_name} {fiche.first_name}"

        elif request.data.get('type') == 'RECHARGEMENT':
            montant = request.data.get('montant')

            if not montant:
                montant = 0
        
            frai, montantTotal, service = calculWithFrais(int(montant), carte.type_carte)

            _montant = montantTotal
            frais = frai

            description = f"Rechargement de la carte {carte.carte_client_id} pour M/mme {fiche.last_name} {fiche.first_name}"


        paiement = Payment.objects.create(
            initiator=request.user.profile,
            carte = carte,
            client = fiche,
            montant=_montant,
            description = description
        )

        operation = Operation.objects.create(
            operation_type= type_operation,
            status_operation = "ATTENTE",
            carte=carte,
            client= fiche,
            payment = paiement,
            operator=request.user.profile,
            montant_operation= _montant,
            montant_initial = _montant,
            frais_operation = frais
        )
        
        apikey = "12662532135d276e2265ca35.50646383"
        site_id = "939314"

        client = Cinetpay(apikey,site_id)

        data = { 
            'amount' : _montant,
            'currency' : "XOF",            
            'transaction_id' : paiement.transaction_id,  
            'description' : description,  
            'return_url' : request.data.get('returnUrl'),
            'notify_url' : "http://visa.mutuelleawoundjo.com/notify/", 
            'customer_name' : fiche.first_name,                              
            'customer_surname' : fiche.last_name,       
        }

        response = client.PaymentInitialization(data)
        _data = response.get('data')
        url = _data.get('payment_url')

        print(url, frais)

    return Response({'payment_url': url})