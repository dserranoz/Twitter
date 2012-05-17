# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from main.forms import UserCreationForm
from main.forms import UserCreateForm
from main.forms import UserForm, UserProfileForm, TweetForm
from main.forms import RegistrationForm, LoginForm
from main.models import UserProfile
from django.contrib.auth.decorators import login_required
from main.models import Tweet


@login_required
def home(request):
    if request.user.is_authenticated():
        return redirect('sesion.html')
    else:
        return render_to_response('home.html', {
    }, RequestContext(request))


def add_User(request):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render_to_response('add_User.html', {
        'form': form,
    }, RequestContext(request))


def User_Registration(request):
    if request.user.is_authenticated():
            return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                    print "Formulario Valido"
                    user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
                    user.save()
#                    users = user.get.profile()
#                    users.name = form.cleaned_data['name']
#                    users.birthday = form.cleaned_data['birthday']
#                    users.save()
#                    users = UserProfile(user=user, birthday=form.cleaned_data['birthday'])
#                   users.save()
                    return redirect('LoginRequest')
            else:
                print "Formulario Invalido"
                return render_to_response('RegisterUser.html', {'form': form}, context_instance=RequestContext(request))
    else:
            ''' user is not submitting the form, show them a blank registration form '''
            form = RegistrationForm()
            context = {'form': form}
            return render_to_response('RegisterUser.html', context, context_instance=RequestContext(request))


def LoginRequest(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        users = authenticate(username=username, password=password)
                        if users is not None:
                                login(request, users)
                                return redirect('sesion')
                        else:
                                return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
                else:
                        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render_to_response('home.html', context, context_instance=RequestContext(request))


def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')


@login_required
def sesion(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
    users = request.user.get_profile()
    tweets = Tweet.objects.all()
    user = UserProfile.objects.filter(user=request.user)[0]
    followings = user.followin.all()
    #notfollowings = UserProfile.objects.exclude(followin__in=list(followings))
    context = {'users': users, 'tweets': tweets, 'followings': followings}
    return render_to_response('sesion.html', context, context_instance=RequestContext(request))


@login_required
def profile(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
    users = request.user.get_profile()
    tweets = Tweet.objects.filter(auth=request.user)
    context = {'users': users, 'tweets': tweets}
    return render_to_response('UserProfile.html', context, context_instance=RequestContext(request))


def password_reset(request):
        return render_to_response('password_reset_form.html', {
    }, RequestContext(request))


def edit_profile(request):
    profile = request.user.get_profile()
    user_form = UserForm(instance=request.user)
    userprofile_form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and userprofile_form.is_valid():
            #assert False, (user_form.cleaned_data, request.user, user_form.save())
            user_form.save()
            userprofile_form.save()
            return redirect('sesion')
    return render_to_response('editprofile.html', {
        'user_form': user_form,
        'userprofile_form': userprofile_form,
    }, RequestContext(request))


def add_tweet(request):
    form = TweetForm()
    auth = TweetForm(instance=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.auth = auth
            tweet.save()
            return redirect('sesion')
    return render_to_response('add_tweet.html', {
        'form': form,
    }, RequestContext(request))


def edit_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    form = TweetForm(instance=tweet)
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('sesion')
    return render_to_response('add_tweet.html', {
        'form': form,
    }, RequestContext(request))


def delete_tweet(request, pk):
    Tweet.objects.filter(pk=pk).delete()
    return redirect('sesion')


def dejar(request, pk):
    user = UserProfile.objects.filter(user=request.user)[0]
    oldfollowing = User.objects.get(pk=pk)
    newfollowing = user.followin.all()
  #  user.pk=None
   # user.id=None
    user.save()
    print ">>>>>"
    print newfollowing
    print "<<<<<<"
    user.followin = newfollowing
    user.save()
    #user.save()
    return redirect('sesion')

