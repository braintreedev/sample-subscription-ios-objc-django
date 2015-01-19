from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^getClientToken', 'serverSubs.views.getClientToken', name='getClientToken'),
    url(r'^getBillPlans', 'serverSubs.views.getBillPlans', name='getBillPlans'),
    url(r'^createSubscription', 'serverSubs.views.createSubscription', name='createSubscription'),
)
