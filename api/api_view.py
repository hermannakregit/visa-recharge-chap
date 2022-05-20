from cinetpay_sdk.s_d_k import Cinetpay
from payment.models import Payment
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User

from operation.utils import calculWithFrais

from .serializers import CarteSerializer, OperationSerializer, FicheSerializer

from operation.models import FraisOperation, Operation, TypeOperation
from user.models import Fiche, Profile

from carte.models import Carte

from user.utils import message

@api_view(['GET'])
def getAllCarte(request):
    
    if request.user.is_authenticated:
        cartes = Carte.objects.filter(owner=None, creator= request.user.profile, type_carte__buy=True)
        serializer = CarteSerializer(cartes, many=True)
        return Response(serializer.data)
    else:
        return Response({
                'statut': '',
                'message': 'You are not authenticated !'
            })

@api_view(['POST'])
def getClientsCards(request):
    
    if request.user.is_authenticated:

        client = request.data.get('client')

        if client is not None:
            
            try:
                fiche = Fiche.objects.get(slug=client)

                cartes = Carte.objects.filter(owner=fiche, creator= request.user.profile)

                serializer = CarteSerializer(cartes, many=True)

                return Response(serializer.data)

            except Fiche.DoesNotExist:
                return Response({
                    'statut': '',
                    'message': 'Client does not exist !'
                })

        cartes = Carte.objects.filter(owner=None, creator= request.user.profile)
        serializer = CarteSerializer(cartes, many=True)
        return Response(serializer.data)
    else:
        return Response({
                'statut': '',
                'message': 'You are not authenticated !'
            })


@api_view(['GET', 'POST'])
def getOperations(request):

    if request.user.is_authenticated:
        
        if request.method == 'POST':
            
            #try:

                #creation d'une opération
                type_operation = TypeOperation.objects.get(name="RECHARGEMENT")
                carte = Carte.objects.get(slug=request.data.get('carte'), type_carte__recharge=True)
                fiche = Fiche.objects.get(owner=carte.owner.owner)

                montant = request.data.get('montant')

                if not montant:
                    montant = 2000
            
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

                serializer = OperationSerializer(operation, many=False)

            #except Carte.DoesNotExist:

            #    return Response({
            #        'statut': '',
            #        'message': 'Impossible to do this !'
            #    })


                return Response({
                    'amount': montant,
                    'operation': serializer.data,
                    'payment_url': url
                })
            
        
        operations = Operation.objects.filter(payment__confirmed=True, status_operation="ATTENTE").exclude(operation_type__name="ACHAT DE CARTE")
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)
        

    else:
        return Response({
            'statut': '',
            'message': 'You are not authenticated !'
        })

@api_view(['GET'])
def getOperationHistory(request):

    if request.user.is_authenticated:
        operations = Operation.objects.filter(payment__confirmed=True, payment__initiator=request.user.profile)
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)
    else:
        return Response({
            'statut': '',
            'message': 'You are not authenticated !'
        })


@api_view(['GET'])
def getOperation(request, slug):
    
    if request.user.is_authenticated:
        try:
            operation = Operation.objects.get(slug=slug)
            serializer = OperationSerializer(operation, many=False)
            return Response(serializer.data)

        except Operation.DoesNotExist:
            return Response({
                'statut': '',
                'message': 'Operation does not exist !'
            })
    else:
        return Response({
            'statut': '',
            'message': 'You are not authenticated !'
        })



@api_view(['POST'])
def operationActions(request):

    VALIDE = "VALIDE"
    ACCEPTE = "ACCEPTE"
    ATTENTE = "ATTENTE"
    
    if request.user.is_authenticated:
        slug = request.data.get('operation')
        action = request.data.get('action')

        try:

            operation = Operation.objects.get(slug=slug)

            if operation.payment.confirmed == True:
                if operation.status_operation == ATTENTE and action.upper() == ACCEPTE:
                    operation.status_operation = ACCEPTE
                elif operation.status_operation == ACCEPTE and action.upper() == VALIDE:
                    operation.status_operation = VALIDE
                else:
                    return Response({
                        'statut': '',
                        'message': 'Impossible to do this opération !'
                    })
                
                operation.save()

            else:
                return Response({
                    'statut': '',
                    'message': 'Impossible to do this opération !'
                })
            
            serializer = OperationSerializer(operation, many=False)
            
            return Response(serializer.data)
            
        except Operation.DoesNotExist:
            return Response({
                'statut': '',
                'message': 'Operation does not exist !'
            })
    else:
        return Response({
            'statut': '',
            'message': 'You are not authenticated !'
        })



@api_view(['POST'])
def createClient(request):

    carte = None
    fiche = None
    type_operation = None
    operation = None
    _montant = None
    url = None

    clients = Fiche.objects.all()

    if request.method == 'POST':
        #print(request.POST)

        if request.user.is_authenticated:
            # verifier la carte envoyé
            try:

                carte = Carte.objects.get(slug=request.data.get('carte'), creator= request.user.profile)

                if carte is not None:
                    
                    try:

                        type_operation = TypeOperation.objects.get(name="ACHAT DE CARTE")
                        frais_op = FraisOperation.objects.get(operation_type = type_operation)
                        _montant = frais_op.buy_carte_amount

                        if request.data.get('client') is not None:

                            #ajouter la cartes

                            try:

                                fiche = Fiche.objects.get(slug=request.data.get('client'))

                            except Fiche.DoesNotExist:
                                return Response({
                                    'statut' : '',
                                    'message': 'Client does not exist !',
                                })

                        else:

                            #print(request.POST)

                            #try: 

                            firstname = request.data.get('firstname')
                            lastname= request.data.get('lastname')
                            email= request.data.get('email')

                            birthPlace= request.data.get('birthPlace')
                            identity = request.data.get('identity')
                            numIdentity= request.data.get('numIdentity')
                            country= request.data.get('country')

                            if not carte.owner:

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

                                username = firstname.lower()[:3] + lastname.lower()[:3]
                                password = f"@{lastname.lower()}@123456"

                                user = User()
                                user.username = username
                                user.first_name = firstname
                                user.last_name = lastname
                                user.email = email
                                user.set_password(password)
                                user.save()

                                _user = User.objects.get(username=username)

                                profile = Profile.objects.get(user=_user)
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

                                message(f"Bonjour M/Mme {lastname} {firstname}, votre inscription a été éffectuée avec succès, vos identifiants sont {username}, mot de pass {password} merci pour votre confiance.", contact)
                            

                                #ajouter la cartes
                                fiche = Fiche.objects.get(owner=_user.profile)

                                #déclenchement de l'operation d'achat de la carte

                             
                            
                        #initialisation du paiement

                        description= f"Achat de carte la carte {carte.carte_client_id} pour M/mme {lastname} {firstname}"
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
                        )
                                
                        apikey = "12662532135d276e2265ca35.50646383"
                        site_id = "939314"

                        client = Cinetpay(apikey,site_id)

                        data = { 
                            'amount' : _montant,
                            'currency' : "XOF",            
                            'transaction_id' : paiement.transaction_id,  
                            'description' : description,  
                            'return_url' : '',
                            'notify_url' : "http://visa.mutuelleawoundjo.com/notify/", 
                            'customer_name' : firstname,                              
                            'customer_surname' : lastname,       
                        }

                        response = client.PaymentInitialization(data)
                        _data = response.get('data')
                        url = _data.get('payment_url')

                        print(url)

                        serializer = FicheSerializer(fiche, many=False)
                        
                        return Response({
                            'payment_url' : url,
                            'client': serializer.data,
                        })
                        
                    except:
                        return Response({
                            'statut': '',
                            'message': 'Error, impossible to register client verify your fields or client duplicate !'
                        })

            except Carte.DoesNotExist:
                return Response({
                    'statut': '',
                    'message': 'Carte does not exist !'
                })
        else:
            return Response({
                'statut': '',
                'message': 'You are not authenticated !'
            })

