# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from main.forms import UserCreationForm


def home(request):
	return render_to_response('home.html', {
	}, RequestContext(request))


def add_User(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render_to_response('add_User.html',{
        'form': form,
    }, RequestContext(request))