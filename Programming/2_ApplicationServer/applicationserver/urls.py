"""applicationserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
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
from django.contrib import admin



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('website.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('user_ballot_registration.urls')),
]

try:
    import accounts.remote_user_add as RemoteAddUser
    server = RemoteAddUser.ServerListener()
    server.start()
except:
    print("Failed to start remote add servive... Failing silently.")

