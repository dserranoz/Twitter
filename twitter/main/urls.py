from django.conf.urls.defaults import patterns, include, url

#Puedes agregar entre las lineas patterns ('main.views'
#para evitar escribir la url completa
urlpatterns = patterns('',
    url(r'^$','main.views.home', name='home'),
    url(r'^user/add/$', 'main.views.add_User', name='add_User' ),
)
