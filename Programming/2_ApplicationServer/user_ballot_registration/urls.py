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
from user_ballot_registration.views import (RegisterForBallot, Vote)

urlpatterns = [
    url(r'^register_for_ballot/(\d{2,5})/$',    RegisterForBallot.as_view(),    name="register_for_ballot"),
    url(r'^vote/(\d{2,5})/$',                   Vote.as_view(),                 name="vote"),
]
