from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from carte.models import Carte
from carte.forms import CarteForm
from carte.utils import serachCartes, paginateCartes


# Create your views here.

@login_required(login_url="login")
def CarteList(request):
    cartes, query = serachCartes(request)
    custom_range, cartes = paginateCartes(request, cartes, 12)

    context = {'cartes' : cartes, 'query': query, 'custom_range': custom_range}
    return render(request, 'cartes/cartes.html', context)


@login_required(login_url="login")
def CarteView(request, slug):
    creator = request.user.profile
    try:
        carte = Carte.objects.get(creator=creator, slug=slug)
    except Carte.DoesNotExist:
        messages.warning(request, "Impossible d'accéder à la page !")
        return redirect('cartes')

    context = {'carte' : carte}
    return render(request, 'cartes/carte.html', context)


@login_required(login_url="login")
def CarteCreate(request):
    page = 'create'
    form = CarteForm()

    if request.method == 'POST':
        form = CarteForm(request.POST)
        num = ''
        if form.is_valid():
            carte = form.save(commit=False)
            carte.creator = request.user.profile
            carte.save()

            num = request.POST['carte_num']

            messages.success(request, f"La carte {num} a été ajoutée avec succès !")
            return redirect('cartes')
        else:
            messages.warning(request, f"La carte {num} n'a pas pu être ajoutée !")
            redirect('create-carte')


    context = {'page': page, 'form' : form}
    return render(request, 'cartes/carte_form.html', context)


@login_required(login_url="login")
def CarteUpdate(request, slug):
    page = 'update'
    creator = request.user.profile
    
    try:
        carte = Carte.objects.get(creator=creator, slug=slug)

        if not carte.owner:
            form = CarteForm(instance=carte)

            if request.method == 'POST':
                form = CarteForm(request.POST, instance=carte)
                if form.is_valid():
                    form.save()
                    messages.success(request, "La carte  a été modifiée avec succès !")
                    redirect('update-carte', slug=carte.slug)
                else:
                    messages.warning(request, "La carte n'a pas pu être modifiée !")
                redirect('update-carte', slug=carte.slug)
        
        else:
            messages.warning(request, f"La carte {carte.carte_num} ne peut etre modifiée !")
            redirect('cartes')

    except Carte.DoesNotExist:
        messages.warning(request, "Impossible d'accéder à la page !")
        return redirect('cartes')

    context = {'page': page, 'carte': carte, 'form' : form}
    return render(request, 'cartes/carte_form.html', context)


@login_required(login_url="login")
def CarteDelete(request, slug):
    creator = request.user.profile
    
    try:
        carte = Carte.objects.get(creator=creator, slug=slug)
        if not carte.owner:
            if request.method == 'POST':
                carte.delete()

                messages.success(request, "La carte a été suprimée avec succès !")
                return redirect('cartes')
        else:
            messages.warning(request, f"La carte {carte.carte_num} ne peut etre suprimée !")
            redirect('cartes')

    except Carte.DoesNotExist:
        messages.warning(request, "Impossible d'accéder à la page !")
        return redirect('cartes')

    context = {'object': carte}
    return render(request, 'delete_object.html', context)