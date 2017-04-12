"""
website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from website.views import (Dashboard, HomepageRedirect)
from user_ballot_registration.views import (RegisterForBallot)

urlpatterns = [

    url(r'^dashboard/$',    Dashboard.as_view(),  name="dashboard"),
    url(r'^$',    HomepageRedirect.as_view(), name="index"),
    url(r'^register_for_ballot/(\d{2,5})/$',    RegisterForBallot.as_view(), name="register_for_ballot"),
    #url(r'^accounts/', include('accounts.urls', namespace='accounts')),
]
