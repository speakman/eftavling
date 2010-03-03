# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from datetime import datetime

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )

if datetime.now() < datetime.strptime(settings.EFVOTE_START, '%Y-%m-%d'):
    urlpatterns += patterns('',
        url(r'^$', 'django.views.generic.simple.direct_to_template', 
            {'template': 'message.html', 'extra_context': {
                    'title': settings.EFVOTE_START_TITLE,
                    'noback': True,
                    'message': settings.EFVOTE_START_MESSAGE}}),
        url(r'.*', 'django.views.generic.simple.redirect_to', 
            {'url': '/'}),
        )
elif datetime.now() > datetime.strptime(settings.EFVOTE_END, '%Y-%m-%d'):
    urlpatterns += patterns('',
        url(r'^$', 'django.views.generic.simple.direct_to_template', 
            {'template': 'message.html', 'extra_context': {
                    'title': settings.EFVOTE_END_TITLE,
                    'noback': True,
                    'message': settings.EFVOTE_END_MESSAGE}}),
        url(r'.*', 'django.views.generic.simple.redirect_to', 
            {'url': '/'}),
        )
else:
    urlpatterns += patterns('',
        url(r'^$', 'django.views.generic.simple.redirect_to', 
            {'url': '/login/'}, name='home'),
        url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'login.html'}, name='login'),
        url(r'^vote/$', 'eftavling.efvote.views.vote', name='vote'),
        url(r'^confirm/$', 'eftavling.efvote.views.confirm', name='confirm'),
        url(r'^results/$', 'eftavling.efvote.views.results', name='stats'),
    )

