from operation.models import FraisOperation, TypeOperation

def my_interval(start, end, value):
    start = int(start)
    end = int(end) + 1
    value = int(value)

    rs = list(range(start, end, 1))

    #print(rs)
    
    if value in rs:
        del rs
        return True
    else:
        del rs
        return False


def calculWithFrais(montant, type_carte):
    service = 100
    montantTotal = None
    frais = None
    _f = None
    frai = None

    type_operation = TypeOperation.objects.get(name="RECHARGEMENT")

    # calculer le montant total
    frais = FraisOperation.objects.filter(
        operation_type=type_operation, 
        carte_type=type_carte
    )

    if frais:

        #on va determiner si c'est le pourcentage ou le montant qui doit etre utilisé

        #print(montant)

        for f in frais:
            #print(f.recharge_fee)

            start = int(f.initial_amount_value)
            end = int(f.final_amount_value) + 1
            montant = int(montant)

            rs = list(range(start, end, 1))
            
            if montant in rs :
                if f.recharge_fee == "montant":
                    _f = f.amount_value
                    montantTotal = montant + _f + service
                    frai = f"{_f} XOF"
                elif f.recharge_fee == "pourcentage":
                    _f = f.percentage_value
                    montantTotal = ((montant * _f) / 100) + montant + service
                    frai = f"{_f} %"

    return frai, montantTotal, service