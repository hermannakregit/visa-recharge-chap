import requests

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from user.models import Fiche


def paginateFiche(request, fiches, results):
    
    page = request.GET.get('p')
    
    paginator = Paginator(fiches, results)

    try:
        fiches = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        fiches = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        fiches = paginator.page(page)

    leftIndex = (int(page) - 3)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 4)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, fiches



def searchFiches(request):
    
    creator = request.user.profile
    query = ''

    if request.GET.get('q'):
        query = request.GET.get('q')
    
    fiches = Fiche.objects.filter( 
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query),
        creator=creator,
    )

    return fiches, query


def message(message, contact):
    url= f'https://ivoiresms.ci/pages/api/smsfree.php'  
    message = f'{message}'
    contact = f'225{contact}'

    data = {
        'login' : "21554002",
        'mdp': "74235532",
        'texte1': message,
        'mobile1': contact,
        'texte2': "",
        'mobile2': "", 
        'texte3': "",
        'mobile3': "", 
        'sender': "",
        'schedule': "",
        'check_mobile_ci': 1,
        'unicode': 1,  
        'tout': 0,
    }

    r = requests.post(url, data = data)
    results = r.json()
    print(results)
