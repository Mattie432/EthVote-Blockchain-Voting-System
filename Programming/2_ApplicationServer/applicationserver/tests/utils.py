# -*- coding: utf-8 -*-
from django.http.request import HttpRequest


def mock_request(ip_address='127.0.0.1'):
    request = HttpRequest()
    request.META['HTTP_CLIENT_IP'] = ip_address
    return request
