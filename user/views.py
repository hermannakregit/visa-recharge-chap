from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from carte.models import Carte
from payment.models import Payment
from operation.models import TypeOperation, Operation, FraisOperation

from user.forms import CustomUserCreationForm, ClientForm
from user.models import Profile, Fiche
from user.utils import paginateFiche, searchFiches

# Create your views here.

def Login(request):

    if request.user.is_authenticated:
        return redirect('cartes')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, "Nom d'utilisateur ou mot de pass incorrect !")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('cartes')
        else:
            messages.warning(request, "Nom d'utilisateur ou mot de pass incorrect !")
            return redirect('login')

    return render(request, 'users/login.html')

def RegisterUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Utilisateur créé avec succès !")
            #return redirect('register')
        else:
            messages.warning(request, "Une erreur est survenue lors de la création de l'utilisateur !")
            #return redirect('register')

    context = {'form': form}
    return render(request, 'users/register_form.html', context)


@login_required(login_url="login")
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def UserProfiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


@login_required(login_url="login")
def UserProfile(request, slug):
    profile = Profile.objects.get(slug=slug)
    context = {'profile': profile}
    return render(request, 'users/profile.html', context)


# gestion des clients
@login_required(login_url="login")
def Clients(request):
    fiches, query = searchFiches(request)
    custom_range, fiches = paginateFiche(request, fiches, 9)

    context = {'fiches': fiches, 'custom_range': custom_range, 'query': query}
    return render(request, 'clients/clients.html', context)

@login_required(login_url="login")
def ClientCreate(request):
    page = 'create'

    form = ClientForm()
    cartes = Carte.objects.filter(creator=request.user.profile, owner=None, type_carte__buy=True)
    carte = None
    fiche = None
    type_operation = None
    operation = None
    _montant = None

    clients = Fiche.objects.all()

    if request.method == 'POST':
        #print(request.POST)
        # verifier la carte envoyé
        try:

            carte = Carte.objects.get(slug=request.POST['carte'], creator= request.user.profile)

            if carte is not None:
                
                #try:

                    type_operation = TypeOperation.objects.get(name="ACHAT DE CARTE")
                    frais_op = FraisOperation.objects.get(operation_type = type_operation, carte_type=carte.type_carte)
                    _montant = frais_op.buy_carte_amount

                    if request.POST.get('client') is not None:
                        
                        #ajouter la cartes
                        fiche = Fiche.objects.get(slug=request.POST.get('client'))

                        if not carte.owner:
                            
                            #déclenchement de l'operation d'achat de la carte

                            operation = Operation.objects.create(
                                operation_type=type_operation,
                                status_operation = "ATTENTE",
                                carte=carte,
                                client= fiche,
                                operator=request.user.profile,
                                montant_operation=_montant,
                                montant_initial = _montant,
                            )
                            
                            messages.success(request, "Procéder au paiment pour finaliser l'attribution de la carte !")
                            #initialisation du paiement
                            paiement = Payment.objects.create(
                                initiator=request.user.profile,
                                carte = carte,
                                operation=operation,
                                client = fiche,
                                montant=_montant,
                                description= f"Achat de carte la carte {carte.carte_client_id} pour M/mme {fiche.last_name} {fiche.first_name}",
                            )
                            return redirect('payment-page', slug=paiement.slug)

                        messages.warning(request, "Cette carte est déjà Attribuée !")
                        return redirect('create-client')

                    else:

                        #print(request.POST)

                        form = ClientForm(request.POST)

                        if form.is_valid(): 

                            if not carte.owner:
                                fiche = form.save(commit=False)
                                fiche.creator = request.user.profile

                                username = fiche.first_name.lower()[:3] + fiche.last_name.lower()[:3]

                                user = User()
                                user.username = username
                                user.first_name = fiche.first_name
                                user.last_name = fiche.last_name
                                user.email = fiche.email
                                user.set_password(f"@{fiche.last_name.lower()}@123456")
                                user.save()

                                _user = User.objects.get(username=username)

                                fiche.owner = _user.profile
                                fiche.save()
                            

                                #ajouter la cartes
                                _fiche = Fiche.objects.get(owner=_user.profile)

                                #déclenchement de l'operation d'achat de la carte
                                
                                operation = Operation.objects.create(
                                    operation_type=type_operation,
                                    status_operation = "ATTENTE",
                                    carte=carte,
                                    client= _fiche,
                                    operator=request.user.profile,
                                    montant_operation=_montant,
                                    montant_initial = _montant,
                                )

                                messages.success(request, "Client enregistré avec succès !")
                                #initialisation du paiement

                                paiement = Payment.objects.create(
                                initiator=request.user.profile,
                                carte = carte,
                                client = _fiche,
                                montant=_montant,
                                description= f"Achat de carte la carte {carte.carte_client_id} pour M/mme {_fiche.last_name} {_fiche.first_name}",
                                )
                                return redirect('payment-page', slug=paiement.slug)
                            
                            messages.warning(request, "Cette carte est déjà Attribuée !")
                            return redirect('create-client')

                        else:
                            messages.warning(request, "Impossible d'enregistrer le client !") 
                            return redirect('create-client')
                #except:
                #    messages.info(request, "Ce client est dèjà enregistré !")
                #    return redirect('create-client')

        except Carte.DoesNotExist:
            messages.warning(request, "Impossible d'enregistrer le client à Nouveau !")
            return redirect('create-client')

    if request.GET.get('c') is not None:
        try:
            carte = Carte.objects.get(slug=request.GET.get('c'))
        except Carte.DoesNotExist:
            carte = None

    context = {'form': form, 'page': page, 'cartes': cartes, 'carte': carte, 'clients': clients}
    return render(request, 'clients/client_form.html', context)


@login_required(login_url="login")
def ClientUpdate(request, slug):
    page = 'update'
    fiche = ''
    cartes = Carte.objects.filter(creator=request.user.profile, owner=None)

    try:

        fiche = Fiche.objects.get(slug=slug, creator= request.user.profile)

        form = ClientForm(instance=fiche)

        if request.method == 'POST':
            form = ClientForm(request.POST, instance=fiche)
            if form.is_valid():
                form.save();

                messages.success(request, "Compte modifié avec success !")
                return redirect('client-profile', slug=fiche.slug)
            else:
                messages.warning(request, "Impossible de modifier le compte 1 !")
                redirect('client-profile', slug=fiche.slug)

    except Fiche.DoesNotExist:
        messages.warning(request, "Impossible de modifier le compte !")
        return redirect('client')

    context = {'form': form, 'fiche': fiche, 'cartes': cartes, 'page': page}
    return render(request, 'clients/client_form.html', context)


#fiche slug passed
@login_required(login_url="login")
def ClientProfile(request, slug):

    creator = request.user.profile
    
    try:
        fiche = Fiche.objects.get(slug=slug, creator=creator)

        #cartes client
        cartes = Carte.objects.filter(owner=fiche)

    except Fiche.DoesNotExist:

        messages.warning(request, "Impossible d'accéder à la page !")
        return redirect('cartes')
    
    context = {'fiche': fiche, 'cartes': cartes}
    return render(request, 'clients/profile.html', context)
