from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
#    t = get_template('current_datetime.html')
#    html = t.render(Context({'current_date' : now}))
#    return HttpResponse(html)
    return render(request, 'current_datetime.html', {'current_datetime' : now } )

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "In %s hour(s), it will be %s." % (offset, dt)
    return HttpResponse(html)
