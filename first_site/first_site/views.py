from django.views import generic


class Main(generic.TemplateView):
    template_name = 'first_site/main.html'

