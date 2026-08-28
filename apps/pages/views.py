from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/home.html"


class ServicesView(TemplateView):
    template_name = "pages/services.html"


class AccountsComingSoonView(TemplateView):
    """
    Stands in for sign-in and sign-up until phase 2 builds real accounts.

    The URL names ``signin`` and ``signup`` are already what the public pages
    link to, so replacing this view later changes no template.
    """

    template_name = "pages/accounts_coming_soon.html"
