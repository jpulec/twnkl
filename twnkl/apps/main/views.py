from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from twnkl.apps.main.forms import MyAuthenticationForm, RegistrationForm, PhotoUploadForm
from twnkl.apps.main.models import Photo, PhotoGroup

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
        if not self.request.user.is_authenticated():
            context['signin_form'] = MyAuthenticationForm()
            context['registration_form'] = RegistrationForm()
        else:
            context['photo_upload_form'] = PhotoUploadForm()
        print context
        return context

class Register(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.backend = 'django.contrib.auth.backends.ModelBackend'
        self.object = form.save()
        auth_login(self.request, self.object)
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(self.get_success_url())

class Profile(ListView):
    template_name = "main/profile.html"
    model = Photo


class Search(ListView):
    template_name = "main/search_results.html"
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context["term"] = self.request.GET.get("term", self.kwargs.get("term", ""))
        return context

    def get_queryset(self):
        return Photo.objects.filter(tags__text__iexact=self.request.GET.get('term', self.kwargs.get("term", "")))

class PhotoView(CreateView):
    model = Photo
    success_url = "/"
    form_class = PhotoUploadForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.owner = User.objects.get(username=self.request.user)
        #form.instance.loc = None
        #tag_objects = []
        #for tag in self.request.POST.get('tags', ""):
        #    tag_objects = [tag_object for tag_object, created in Tag.objects.get_or_create(text=tag)]
        #form.instance.tags = tag_objects
        #form.instance.group = PhotoGroup.objects.get_or_create(name=self.request.POST.get('group', ''), user=User.objects.get(username=self.request.user))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PhotoView, self).form_valid(form)
