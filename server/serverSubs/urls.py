from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^getClientToken', 'serverSubs.views.get_client_token', name='getClientToken'),
    url(r'^getBillPlans', 'serverSubs.views.get_bill_plans', name='getBillPlans'),
    url(r'^createSubscription', 'serverSubs.views.create_subscription', name='createSubscription'),
)
