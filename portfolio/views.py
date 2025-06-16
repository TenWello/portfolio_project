from django.views import View
from django.http import Http404
from django.views.generic import ListView, DetailView

from django.shortcuts import render
from django.views.generic import TemplateView
from portfolio.models import AboutMe, Experience, Education, Skill, Project, Service


def index(request):
    return render(request, 'template/index.html')

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # about_me = AboutMe.objects.select_related('user').first()  # Bitta AboutMe obyektini olish
        context['about_me'] = AboutMe.objects.select_related('user').first()
        context['experiences'] = Experience.objects.filter(about_me=context['about_me'])
        context['educations'] = Education.objects.filter(about_me=context['about_me'])  # To'liq queryset olish

        return context

class CredentialsView(TemplateView):
    template_name = 'credentials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()
        context['about_me'] = about_me
        context['experiences'] = Experience.objects.filter(about_me=about_me) if about_me else {}
        context['educations'] = Education.objects.filter(about_me=about_me)
        context['social_media'] = about_me.social_media if about_me else {}
        context['skills'] = Skill.objects.all()  # Barcha skill larni olish


        return context

class WorksView(ListView):
    model = Project
    template_name = 'works.html'
    context_object_name = 'projects'
    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')

class WorksDetailView(DetailView):
    model = Project
    template_name = 'works-detail.html'
    context_object_name = 'project'
    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')
    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        try:
            return Project.objects.prefetch_related('images').get(slug=slug)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")


def service_page(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'service.html', context)


