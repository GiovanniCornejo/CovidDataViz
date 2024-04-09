from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Store csv data globally
import csv
def load_csv_data():
    with open("data/covid-data-10-16-20.csv", 'r') as csvfile:
        return [line for line in csv.DictReader(csvfile)]
data = load_csv_data()

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'visualization/home.html')

def us_cases(request: HttpRequest) -> HttpResponse:
    # TODO: Implement us_cases view
    print("TODO: Implement us_cases view")
    return render(request, "visualization/us_cases.html")

def avg_cases_and_deaths(request: HttpRequest) -> HttpResponse:
    # TODO: Implement avg_cases_and_deaths view
    print("TODO: Implement avg_cases_and_deaths view")
    return render(request, "visualization/avg_cases_and_deaths.html")

def top5_radar(request: HttpRequest) -> HttpResponse:
    # TODO: Implement top5_radar view
    print("TODO: Implement top5_radar view")
    return render(request, "visualization/top5_radar.html")

def max_diff(request: HttpRequest) -> HttpResponse:
    # TODO: Implement max_diff view
    print("TODO: Implement max_diff view")
    return render(request, "visualization/max_diff.html")

def positive_rates(request: HttpRequest) -> HttpResponse:
    # TODO: Implement positive_rates view
    print("TODO: Implement positive_rates view")
    return render(request, "visualization/positive_rates.html")