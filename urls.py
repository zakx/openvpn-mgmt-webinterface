from django.conf.urls.defaults import *
from django.contrib import auth
from django.conf import settings
from purple.app.models import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
	url(r'^accounts/login/$', 'login', {'template_name': 'core/login.html'}, name="login"),
	url(r'^accounts/logout/$', 'logout', {'template_name': 'core/logout.html'}, name="logout"),
	url(r'^accounts/pwchange/$', 'password_change', {'template_name': 'core/pwchange.html','post_change_redirect': '/accounts/pwchange/done/',}, name="pwchange"),
	url(r'^accounts/pwchange/done/$', 'password_change_done', {'template_name': 'core/pwchange_done.html'}, name="pwchange-done"),
	url(r'^accounts/pwreset/$', 'password_reset', {'template_name': 'core/pwreset.html','post_reset_redirect': '/accounts/pwreset/done/',}, name="pwreset"),
	url(r'^accounts/pwreset/done/$', 'password_reset_done', {'template_name': 'core/pwreset_done.html'}, name="pwreset-done"),
	url(r'^accounts/pwreset/confirm/(?P<token>(.+))/(?P<uidb36>(.+))/$', 'password_reset_confirm', {'template_name': 'core/pwreset_confirm.html'}, name="pwreset-confirm"),
	url(r'^accounts/pwreset/complete/$', 'password_reset_complete', {'template_name': 'core/pwreset_complete.html'}, name="pwreset-complete"),
)

urlpatterns += patterns('purple.app.views',
	url(r'^$', 'welcome_view', name='welcome'),
	url(r'^status/$', 'status_view', name='status'),
	url(r'^user/(?P<user_id>(\d+))/kill/$', 'kill_action', name="kill"),
	url(r'^user/(?P<user_id>(\d+))/ban/$', 'ban_action', name="ban"),
)

urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False }),
	(r'^admin/', include(admin.site.urls)),
)
