from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Store csv data globally
import pandas as pd
covid_df = pd.read_csv("data/covid-data-10-16-20.csv")

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'visualization/home.html')

def us_cases(request: HttpRequest) -> HttpResponse:
    """
    Generate a double line graph visualization that plots the total and new number of COVID cases 
    in the United States where data is available (no null values) over time.

    Return:
    `labels`: The dates for the data.
    `total_cases`: Total number of cases for those dates.
    `new_cases`: New number of cases for those dates. 
    """
    us_cases = covid_df[
        (covid_df["iso_code"] == "USA") & covid_df["total_cases"] & covid_df["new_cases_smoothed"]
    ]

    return render(request, "visualization/us_cases.html", 
        context={ 
            "labels": us_cases["date"].tolist(), 
            "total_cases": us_cases["total_cases"].tolist(),
            "new_cases": us_cases["new_cases_smoothed"].tolist()
        }
    )

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