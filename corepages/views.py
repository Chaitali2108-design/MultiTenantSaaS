from django.shortcuts import render, redirect


def home(request):
    return render(
        request,
        "corepages/home.html",
    )


def features(request):

    return render(
        request,
        "corepages/features.html"
    )