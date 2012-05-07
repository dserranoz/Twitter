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
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
