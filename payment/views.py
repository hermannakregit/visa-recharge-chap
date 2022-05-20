from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from operation.models import Operation

from payment.models import Payment
from user.utils import message

from payment.utils import getCinetpayTransaction

# Create your views here.

@login_required(login_url='login')
def PaymentPage(request, slug):

    context= {}

    try:
        payment = Payment.objects.get(slug=slug)

        #initiator

        context= {'payment': payment }

    except Payment.DoesNotExist:
        return redirect('clients')

    return render(request, 'payments/payment.html', context)


@login_required(login_url='login')
def GetPayment(request, slug):

    try:

        payment = Payment.objects.get(slug=slug)

    except Payment.DoesNotExist:

        messages.warning(request, "Impossible de traiter l'opération !")
        return redirect('clients')

    data = getCinetpayTransaction(payment.transaction_id)

    state = data.get('data')

    if state.get('status') == 'ACCEPTED' and payment.confirmed == False:
        #print(data)

        # Modification du paiement
        payment.code = data.get('code')
        payment.message = data.get('message')
        payment.cash = state.get('currency')
        payment.status = state.get('status')
        payment.confirmed = True
        payment.payment_method = state.get('payment_method')
        payment.description = state.get('description')
        payment.metadata = state.get('metadata')
        payment.operator_id = state.get('operator_id')
        payment.api_response_id = state.get('api_response_id')
        payment.payment_date = state.get('payment_date')
        payment.save()

        # attribution de la carte !
        carte = payment.carte
        if not carte.owner:
            carte.owner = payment.client
            carte.status = True
            carte.save()
        
        #Ajout de l'opération d'achat de carte
        operation = Operation.objects.get(payment=payment)
        operation.status_operation = "VALIDE"
        operation.date_acceptation = payment.date_added
        operation.date_validation = payment.payment_date
        operation.save()

        message(
            message = f"Bonjour M/Mme {payment.client.first_name} {payment.client.last_name}, votre opéraation est en cour de traitement, Merci de votre confiance.",
            contact= payment.client.contact_one
        )
        
    context= {'payment': payment}

    return render(request, 'payments/paymentRecu.html', context)



def notificationURl(request):

    #if request.method == 'POST':

        transaction_id = request.data.get('cpm_trans_id')

        message(
                message = transaction_id,
                contact= '0758237837'
            )

        try:

            payment = Payment.objects.get(transaction_id=transaction_id)

        except Payment.DoesNotExist:
           return HttpResponse('Error')

        data = getCinetpayTransaction(payment.transaction_id)

        state = data.get('data')

        # Modification du paiement
        payment.code = data.get('code')
        payment.message = data.get('message')
        payment.cash = state.get('currency')
        payment.status = state.get('status')
        payment.confirmed = True
        payment.payment_method = state.get('payment_method')
        payment.description = state.get('description')
        payment.metadata = state.get('metadata')
        payment.operator_id = state.get('operator_id')
        payment.api_response_id = state.get('api_response_id')
        payment.payment_date = state.get('payment_date')
        payment.save()

        if state.get('status') == 'ACCEPTED' and payment.confirmed == False:
            #print(data)

            operation = Operation.objects.get(payment=payment)
            operation.status_operation = "VALIDE"

            # attribution de la carte !
            carte = payment.carte
            if not carte.owner:
                carte.owner = payment.client
                carte.status = True
                carte.save()

                operation.date_acceptation = payment.date_added
                operation.date_validation = payment.payment_date
            
            operation.save()

            message(
                message = f"Bonjour M/Mme {payment.client.first_name} {payment.client.last_name}, votre opération est en cour de traitement, Merci de votre confiance.",
                contact= payment.client.contact_one
            )
        
            return HttpResponse('Success')

        return HttpResponse('Error')


def forceNotificationURl(request):

    payments = Payment.objects.all()

    for p in payments:

        payment = None

        try:

            payment = Payment.objects.get(slug=p.slug)

        except Payment.DoesNotExist:
           return HttpResponse('Error')

        data = getCinetpayTransaction(payment.transaction_id)

        state = data.get('data')

        # Modification du paiement
        payment.code = data.get('code')
        payment.message = data.get('message')
        payment.cash = state.get('currency')
        payment.status = state.get('status')
        payment.confirmed = True
        payment.payment_method = state.get('payment_method')
        payment.description = state.get('description')
        payment.metadata = state.get('metadata')
        payment.operator_id = state.get('operator_id')
        payment.api_response_id = state.get('api_response_id')
        payment.payment_date = state.get('payment_date')
        payment.save()

        if state.get('status') == 'ACCEPTED' and payment.confirmed == False:
            #print(data)

            operation = Operation.objects.get(payment=payment)
            operation.status_operation = "VALIDE"

            # attribution de la carte !
            carte = payment.carte
            if not carte.owner:
                carte.owner = payment.client
                carte.status = True
                carte.save()

                operation.date_acceptation = payment.date_added
                operation.date_validation = payment.payment_date
            
            operation.save()

            message(
                message = f"Bonjour M/Mme {payment.client.first_name} {payment.client.last_name}, votre opération est en cour de traitement, Merci de votre confiance.",
                contact= payment.client.contact_one
            )
        
        return HttpResponse('Success')

    return HttpResponse('Success')

