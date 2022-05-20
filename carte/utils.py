from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from carte.models import Carte


def paginateCartes(request, cartes, results):
    
    page = request.GET.get('p')
    
    paginator = Paginator(cartes, results)

    try:
        cartes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        cartes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        cartes = paginator.page(page)

    leftIndex = (int(page) - 3)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 4)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, cartes



def serachCartes(request):
    
    creator = request.user.profile
    query = ''

    if request.GET.get('q'):
        query = request.GET.get('q')
    
    cartes = Carte.objects.filter( 
        Q(carte_client_id__icontains=query) |
        Q(carte_num__icontains=query) |
        Q(carte_exp_month__icontains=query) |
        Q(carte_exp_year__icontains=query),
        creator=creator,
    )

    return cartes, query