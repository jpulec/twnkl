from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from twnkl.apps.main.views import Home, Login, Logout, Register, Profile, Search, PhotoView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', Login.as_view(), name="my_login"),
    url(r'^logout/$', Logout.as_view(), name="my_logout"),
    url(r'^register/$', Register.as_view(), name="register"),
    url(r'^search/$', Search.as_view(), name="search"),
    url(r'^search/(?P<term>\w+)/$', Search.as_view(), name="search"),
    url(r'^photos/$', PhotoView.as_view(), name="photo"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', Profile.as_view(), name="profile"),
    url(r'^accounts/profile/(?P<username>\w+)/$', Profile.as_view(), name="profile"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Static-y pages
    #url(r'^about/$', About.as_view(), name="about"),
    #url(r'^contact/$', Contact.as_view(), name='contact'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
