from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'visualization/home.html')

def us_cases(request: HttpRequest) -> HttpResponse:
    # TODO: Implement us_cases view
    print("TODO: Implement us_cases view")
    return redirect('home')

def avg_cases_and_deaths(request: HttpRequest) -> HttpResponse:
    # TODO: Implement avg_cases_and_deaths view
    print("TODO: Implement avg_cases_and_deaths view")
    return redirect('home')

def top5_radar(request: HttpRequest) -> HttpResponse:
    # TODO: Implement top5_radar view
    print("TODO: Implement top5_radar view")
    return redirect('home')

def max_diff(request: HttpRequest) -> HttpResponse:
    # TODO: Implement max_diff view
    print("TODO: Implement max_diff view")
    return redirect('home')

def positive_rates(request: HttpRequest) -> HttpResponse:
    # TODO: Implement positive_rates view
    print("TODO: Implement positive_rates view")
    return redirect('home')