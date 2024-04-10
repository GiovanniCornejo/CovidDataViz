from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from numpy import positive

from .forms import MonthForm

import pandas as pd

# Store csv data globally
covid_df = pd.read_csv("data/covid-data-10-16-20.csv")
covid_df["month"] = pd.to_datetime(covid_df["date"]).dt.month

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "visualization/home.html")

def us_cases(request: HttpRequest) -> HttpResponse:
    """
    Generates a double line graph visualization that plots the total and new number of COVID cases 
    in the United States where data is available (no null values) over time.

    Return:
    `labels`: The dates for the data.
    `total_cases`: Total number of cases for those dates.
    `new_cases`: New number of cases for those dates. 
    """
    us_cases = covid_df[
        (covid_df["iso_code"] == "USA") & covid_df["total_cases"] & covid_df["new_cases_smoothed"]
    ]

    return render(request, "visualization/us_cases.html", { 
        "labels": us_cases["date"].tolist(), 
        "total_cases": us_cases["total_cases"].tolist(),
        "new_cases": us_cases["new_cases_smoothed"].tolist()
    })

def avg_cases_and_deaths(request: HttpRequest) -> HttpResponse:
    """
    Generates a stacked bar graph visualization to show: For which month did each country have the
    highest on average daily new cases along with how many total deaths happened in this month.
    Plots the top 5 countries with the most new cases.

    Return:
    `labels`: The country names.
    `new_cases`: Average number of daily cases that month.
    `new_deaths`: Total number of new deaths that month.
    """    
    # Filter out non-country locations
    df = covid_df[(covid_df["location"] != "International") & (covid_df["location"] != "World")]

    monthly_country_data = df.groupby(["location", "month"]).agg(
        avg_cases=("new_cases", "mean"),
        new_deaths=("new_deaths", "sum")
    ).dropna(subset=["avg_cases", "new_deaths"])

    # Filter each country to month with highest average daily cases
    highest_avg_daily_cases = monthly_country_data.groupby("location")["avg_cases"].idxmax()
    highest_monthly_country_data = monthly_country_data.loc[highest_avg_daily_cases]

    # Get top 5 countries with highest average daily new cases in one month
    top5_countries = highest_monthly_country_data["avg_cases"].nlargest(5).index.get_level_values("location")
    avg_cases = highest_monthly_country_data.loc[top5_countries, "avg_cases"]
    new_deaths = highest_monthly_country_data.loc[top5_countries, "new_deaths"]

    return render(request, "visualization/avg_cases_and_deaths.html", {
        "labels": top5_countries.tolist(),
        "new_cases": avg_cases.tolist(),
        "new_deaths": new_deaths.tolist()
    })

def top5_radar(request: HttpRequest) -> HttpResponse:
    """
    Generates a radar chart visualization to compare data of the top five
    countries with the most total cases.

    Return:
    `label`: The country names.
    `cases`: Total cases for each country (in ten thousands).
    `deaths`: Total deaths for each country (in thousands).
    `cases_per_million`: Cases per million.
    `deaths_per_million`: Deaths per million * 100 for each country (for scaling).
    """
    # Filter out non-country locations
    df = covid_df[(covid_df["location"] != "International") & (covid_df["location"] != "World")] 

    total_country_data = df.groupby("location")[["total_cases", "total_deaths", "total_cases_per_million", "total_deaths_per_million"]].max()
    top5_countries = total_country_data.nlargest(5, "total_cases")
    
    # Scale necessary columns
    top5_countries["total_cases"] //= 10_000
    top5_countries["total_deaths"] //= 1_000
    top5_countries["total_deaths_per_million"] *= 100

    return render(request, "visualization/top5_radar.html", {
        "labels": top5_countries.index.tolist(),
        "cases": top5_countries["total_cases"].tolist(),
        "deaths": top5_countries["total_deaths"].tolist(),
        "cases_per_million": top5_countries["total_cases_per_million"].tolist(),
        "deaths_per_million": top5_countries["total_deaths_per_million"].tolist()
    })

def max_diff(request: HttpRequest) -> HttpResponse:
    """
    Generates a bar graph visualization for the difference in the total number of new cases in the 
    top 5 countries with the most total cases before (including May) and after May (starting June).

    Return:
    `labels`: The country names.
    `differences`: The difference between the total cases before and after May (absolute values)
    """
    # Filter out non-country locations
    df = covid_df[(covid_df["location"] != "International") & (covid_df["location"] != "World")] 

    before_may_cases = df[df["month"] <= 5].groupby("location")["new_cases"].max()
    after_may_cases = df[df["month"] > 5].groupby("location")["new_cases"].max()
    differences = (after_may_cases - before_may_cases).abs()

    top5_countries = differences.nlargest(5)

    return render(request, "visualization/max_diff.html", {
        "labels": top5_countries.index.tolist(),
        "differences": top5_countries.tolist()
    })

def positive_rates(request: HttpRequest) -> HttpResponse:
    """
    Ask users to input a month in numeric format (e.g., March = 3). Then, generates a pie chart visualization to compare the 
    top 5 countries with the highest total cases and find the average positive rate in those countries for the specified month.

    Return:

    `labels`: The country names.
    `positive_rates`: The average positive rate in that month for each country (in percents, i.e., * 100)
    """
    if request.method == "POST":
        form = MonthForm(request.POST)
        if form.is_valid():
            month: int = form.cleaned_data["month"]

            # Filter out non-country locations and to current month
            df = covid_df[(covid_df["location"] != "International") & (covid_df["location"] != "World") & (covid_df["month"] == month)] 

            top5_countries = df.groupby("location")["total_cases"].max().nlargest(5)
            
            # Filter out countries with zero positive rates
            top5_countries = top5_countries[top5_countries.index.isin(df[df["positive_rate"] > 0]["location"])]

            average_positive_rates = []
            for country in top5_countries.index:
                positive_rates = df[df["location"] == country]["positive_rate"]   
                average_positive_rates.append(positive_rates.mean() * 100)

            # Render the template with the data
            return render(request, "visualization/positive_rates.html", {
                "form": form,
                "labels": top5_countries.index.tolist(),
                "positive_rates": average_positive_rates
            })
    else:
        form = MonthForm()
    
    # If form is not valid or it's a GET request, render the form with errors or empty form
    return render(request, "visualization/positive_rates.html", {
        "form": form
    })
