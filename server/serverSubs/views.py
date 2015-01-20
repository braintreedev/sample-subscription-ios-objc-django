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

def get_client_token(request):

    clientToken=braintree.ClientToken.generate({})

    responseData = {}
    responseData['clientToken'] = clientToken
    return HttpResponse(json.dumps(responseData), content_type="application/json")

def get_bill_plans(request):
    billPlans=braintree.Plan.all()

    planIDs   = []
    for simplePlan in billPlans:
        planIDs.append(simplePlan.id)

    responseData = {}
    responseData['planIDs'] = planIDs
    return HttpResponse(json.dumps(responseData), content_type="application/json")

def create_subscription(request):

    """
    " Creating the costumer and adding payment_method_nonce
    """
    result = braintree.Customer.create({
        "first_name": " ",
        "last_name": " ",
    })

    if result.is_success:
        customerId = result.customer.id

        """
        " Creating the subscription
        """
        resultPaymentMethod = braintree.PaymentMethod.create({
            "customer_id": customerId,
            "payment_method_nonce": request.POST.get("payment_method_nonce"),
        })

        paymentMethodToken = resultPaymentMethod.payment_method.token

        resultSubscription = braintree.Subscription.create({
            "payment_method_token": paymentMethodToken,
            "plan_id": request.POST.get("plan_id"),
        })

        if resultSubscription.is_success:
            responseData = {}
            responseData['subscription_id'] = resultSubscription.subscription.id
            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            return "Error: {0}".format(result.message)
    else:
        return "Error: {0}".format(result.message)
