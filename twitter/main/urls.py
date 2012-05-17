from django.conf.urls.defaults import patterns, include, url

#Puedes agregar entre las lineas patterns ('main.views'
#para evitar escribir la url completa
urlpatterns = patterns('',
    url(r'^$','main.views.home', name='home'),
    url(r'^user/add/$', 'main.views.add_User', name='add_User' ),
    url(r'^user/Register/$', 'main.views.User_Registration', name='User_Registration' ),
    url(r'^user/login/$', 'main.views.LoginRequest', name='LoginRequest' ),
    url(r'^user/logout/$', 'main.views.LogoutRequest', name='LogoutRequest' ),
    url(r'^user/sesion/$', 'main.views.sesion', name='sesion' ),
    url(r'^user/profile/$', 'main.views.profile', name='profile' ),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^user/profile/edit/$', 'main.views.edit_profile', name='edit_profile' ),
    url(r'^tweet/add/$', 'main.views.add_tweet', name='add_tweet'),
    url(r'^tweet/(?P<pk>\d+)/edit$', 'main.views.edit_tweet', name='edit_tweet'),
    url(r'^tweet/(?P<pk>\d+)/delete$', 'main.views.delete_tweet', name='delete_tweet'),
    url(r'^dejar/(?P<pk>\d+)/$', 'main.views.dejar', name='dejar'),
)
