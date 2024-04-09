from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("us_cases", views.us_cases, name="us_cases"),
    path("avg_cases_and_deaths", views.avg_cases_and_deaths, name="avg_cases_and_death"),
    path("top5_radar", views.top5_radar, name="top5_radar"),
    path("max_diff", views.max_diff, name="max_diff"),
    path("positive_rates", views.positive_rates, name="positive_rates")
]
