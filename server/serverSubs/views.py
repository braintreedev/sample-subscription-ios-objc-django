"""
" views.py
" --------
" To use Braintree it is mandatory to configure the API credentials, that could
" be gotten from Braintree account. In this example, we'll use Sandbox API
" credentials from the Commerce Factory Braintree account. More information at:
"    * github.com/commercefactory
"    * commercefactory.org
"""

import braintree
import json

from django.http import HttpResponse
from django.core import serializers

"""
" Space reserved for configuration.
" 1. API credentials to use Braintree
" 2. API credentials to use Spark core
"""

braintree.Configuration.configure(
                braintree.Environment.Sandbox,
                merchant_id="ffdqc9fyffn7yn2j",
                public_key="qj65nndbnn6qyjkp",
                private_key="a3de3bb7dddf68ed3c33f4eb6d9579ca"
                )


"""
" Getting the client_token, which contains
" all authorization and configuration information your client needs to
" initialize a Braintree Client SDK to communicate with Braintree.
"""

def getClientToken(request):

    clientToken=braintree.ClientToken.generate({})

    response_data = {}
    response_data['clientToken'] = clientToken
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def getBillPlans(request):
    billPlans=braintree.Plan.all()

    planIDs   = []
    for simplePlan in billPlans:
        planIDs.append(simplePlan.id)

    response_data = {}
    response_data['planIDs'] = planIDs
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def createSubscription(request):
    result = braintree.Customer.create({
        "first_name": " ",
        "last_name": " ",
        "payment_method_nonce": request.POST.get("payment_method_nonce"),
    })

    if result.is_success:
        try:
            customer_id = result.customer.id
            customer = braintree.Customer.find(customer_id)
            payment_method_token = customer.credit_cards[0].token
            result = braintree.Subscription.create({
                "payment_method_token": payment_method_token,
                "plan_id": request.POST.get("plan_id"),
            })
            if result.is_success:
                response_data = {}
                response_data['subscription_id'] = result.subscription.id
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return "Error: {0}".format(result.message)
        except braintree.exceptions.NotFoundError:
            return "No customer found for id: {0}".format(request.args['id'])
    else:
        return "Error: {0}".format(result.message)
