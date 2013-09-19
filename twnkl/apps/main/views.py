from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from twnkl.apps.main.forms import MyAuthenticationForm, RegistrationForm, PhotoUploadForm, PhotoUpdateForm
from twnkl.apps.main.models import Photo, PhotoGroup
from geoposition import Geoposition
from PIL import Image
from PIL.ExifTags import TAGS

import logging
logger = logging.getLogger(__name__)

class Login(FormView):
    form_class = MyAuthenticationForm
    template_name = "main/signin.html"
    success_url = "/"

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)

class Logout(RedirectView):
    url = "/"

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(self.get_redirect_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Logout, self).dispatch(*args, **kwargs)

class Home(ListView):
    template_name = "main/home.html"
    model = Photo

    def get_queryset(self):
        photos = []
        threshold = 0.5
        for photo in Photo.objects.all():
            if pow(pow(float(photo.loc.latitude), 2) + pow(float(photo.loc.longitude), 2), 0.5) < threshold:
                photos.append(photo)
        return photos

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['recent_list'] = Photo.objects.order_by('-dt')[0:20]
        print context['recent_list']
        if not self.request.user.is_authenticated():
            context['signin_form'] = MyAuthenticationForm()
            context['registration_form'] = RegistrationForm()
        else:
            context['photo_upload_form'] = PhotoUploadForm(user=self.request.user.username)
        return context

class Register(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.backend = 'django.contrib.auth.backends.ModelBackend'
        self.object = form.save()
        group = PhotoGroup(owner=self.object, name="default")
        group.save()
        auth_login(self.request, self.object)
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(self.get_success_url())

class Profile(ListView):
    template_name = "main/profile.html"
    model = PhotoGroup

    def get_queryset(self):
        if 'username' in self.kwargs:
            get_object_or_404(User, username=self.kwargs['username'])
            return PhotoGroup.objects.filter(owner__username=self.kwargs['username'])
        return PhotoGroup.objects.filter(owner__username=self.request.user.username)

class Search(ListView):
    template_name = "main/search_results.html"
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["term"] = self.request.GET.get("term", self.kwargs.get("term", ""))
        return context

    def get_queryset(self):
        return Photo.objects.filter(tags__text__iexact=self.request.GET.get('term', self.kwargs.get("term", "")))

class PhotosView(ListView):
    model = Photo
    template_name = "main/photos_view.html"

    def get_context_data(self, **kwargs):
        context = super(PhotosView, self).get_context_data(**kwargs)
        context['group_name'] = PhotoGroup.objects.get(owner__username=self.kwargs.get('owner', self.request.user.username), name=self.kwargs.get('name', 'default')).name
        return context

    def get_queryset(self):
        group = PhotoGroup.objects.filter(owner__username=self.kwargs.get('owner', self.request.user.username), name=self.kwargs.get('name', 'default'))
        return Photo.objects.filter(groups=group)

class PhotoView(UpdateView):
    model = Photo
    template_name = "main/photo_view.html"
    form_class = PhotoUpdateForm

    def get_success_url(self):
        return force_text(self.request.META['HTTP_REFERER'])

    def get_form_kwargs(self):
        kwargs = super(PhotoView, self).get_form_kwargs()
        kwargs['user'] = self.request.user.username
        return kwargs

class UploadPhotoView(CreateView):
    model = Photo
    success_url = "/accounts/profile/"
    form_class = PhotoUploadForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.owner = User.objects.get(username=self.request.user)
        #tag_objects = []
        #for tag in self.request.POST.get('tags', ""):
        #    tag_objects = [tag_object for tag_object, created in Tag.objects.get_or_create(text=tag)]
        #form.instance.tags = tag_objects
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid()

    def form_valid(self, form):
        exif_data = self.get_exif(form.instance.image)
        if "GPSInfo" in exif_data:
            if 2 in exif_data['GPSInfo'] and 4 in exif_data['GPSInfo']:
                form.instance.loc = Geopostion(exif_data['GPSInfo'][2], exif_data['GPSInfo'][4]) 
        form.save()
        return super(UploadPhotoView, self).form_valid(form)

    def form_invalid(self):
        return HttpResponseRedirect("/")

    def get_form_kwargs(self):
        kwargs = super(UploadPhotoView, self).get_form_kwargs()
        kwargs['user'] = self.request.user.username
        return kwargs

    def get_exif(self, fn):
        ret = {}
        try:
            i = Image.open(fn)
            info = i._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
        except AttributeError as e:
            pass
        return ret
