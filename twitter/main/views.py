# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.template import RequestContext


def home(request):
	return render_to_response('home.html', {
	}, RequestContext(request))