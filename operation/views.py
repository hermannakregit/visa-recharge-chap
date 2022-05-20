from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from operation.forms import OperationForm
from carte.models import Carte

from payment.models import Payment
from operation.models import TypeOperation, Operation

from operation.utils import calculWithFrais, my_interval

# Create your views here.

@login_required(login_url="login")
def ClientOperations(request, slug):

    return render(request, 'operations/client.html')



@login_required(login_url="login")
def OperationCreate(request, slug):
    page = 'create'
    form = OperationForm()
    carte = None
    montant = None
    montantTotal = None
    frai = None
    service = None

    try:
        carte = Carte.objects.get(slug=slug)
    except Carte.DoesNotExist:
        messages.warning(request, "Impossible de traiter la requete")
        return redirect('cartes')

    if request.method == 'POST':

        form = OperationForm(request.POST)

        if form.is_valid():

            # action de résumé de paiement
            operation = form.save(commit=False)

            if operation.montant_operation is not None:

                montant = operation.montant_operation

                v = my_interval(carte.type_carte.initial, carte.type_carte.plafond, montant)

                if v == True :

                    frai, montantTotal, service = calculWithFrais(montant, carte.type_carte)

                    page = "resume"

                else:
                    messages.warning(request, f"Le montant de rechargement doit etre entre 2000 et {carte.type_carte.plafond} XOF ")
                    return redirect('create-operation', slug=slug)

            else:
                messages.warning(request, "Le montant de rechargement doit etre superieur à 2000 XOF")
                return redirect('create-operation', slug=slug)


            """   car = form.save(commit=False)
                carte.creator = request.user.profile
                carte.save() """

        else:
            messages.warning(request, "Impossible de traiter la requete")
            return redirect('create-operation', slug=slug)

    context = {'page': page, 'form' : form, 'carte' : carte, 'montantTotal': montantTotal, 'montant': montant, 'frais': frai, 'service': service}
    return render(request, 'operations/operation_form.html', context)

@login_required(login_url="login")
def OperationPayment(request):

    carte = None

    try:
        carte = Carte.objects.get(slug=request.POST['slug'])
    except Carte.DoesNotExist:
        messages.warning(request, "Impossible de traiter la requete")
        return redirect('cartes')

    type_operation = TypeOperation.objects.get(name="RECHARGEMENT")
    
    #déclenchement de l'operation d'achat de la carte

    frai, montantTotal, service = calculWithFrais(int(request.POST['montant']), carte.type_carte)

    paiement = Payment.objects.create(
        initiator=request.user.profile,
        carte = carte,
        client = carte.owner,
        montant= montantTotal,
        description= f" Rechargement de carte la carte {carte.carte_client_id} pour M/mme {carte.owner.last_name} {carte.owner.first_name}",
    ) 

    operation = Operation.objects.create(
        operation_type=type_operation,
        status_operation = "ATTENTE",
        carte=carte,
        client= carte.owner,
        payment=paiement,
        operator=request.user.profile,
        montant_operation= montantTotal,
        montant_initial = int(request.POST['montant']),
        frais_operation = frai,
    )
    return redirect('payment-page', slug=paiement.slug)
