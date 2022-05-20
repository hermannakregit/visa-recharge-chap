from cinetpay_sdk.s_d_k import Cinetpay

def getCinetpayTransaction(transaction_id):
    apikey = "12662532135d276e2265ca35.50646383"
    site_id = "939314"

    client = Cinetpay(apikey,site_id)

    data = client.TransactionVerfication_trx(transaction_id)
   
    return data