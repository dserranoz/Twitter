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
#imports for reset password
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site


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
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save()
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


# my views for change password


@csrf_protect
def password_reset_(request, is_admin_site=False,
                   template_name='password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done_')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.META['HTTP_HOST'])
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))


def password_reset_done_(request,
                        template_name='password_reset_done_.html',
                        current_app=None, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))


@never_cache
def password_reset_confirm_(request, uidb36=None, token=None,
                           template_name='password_reset_confirm_.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb36 is not None and token is not None
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))


def password_reset_complete_(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': settings.LOGIN_URL
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))
