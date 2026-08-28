from django.urls import path

from .views import AccountsComingSoonView, HomeView, ServicesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("services/", ServicesView.as_view(), name="services"),
    # Replaced by real authentication views in phase 2. The names are final.
    path("sign-in/", AccountsComingSoonView.as_view(), name="signin"),
    path("sign-up/", AccountsComingSoonView.as_view(), name="signup"),
]
