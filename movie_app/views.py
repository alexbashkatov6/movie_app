from django.shortcuts import render, get_object_or_404
from django.db.models import F, Sum, Min, Max, Count, Avg, Value

# Create your views here.
from .models import Movie


def show_all_movie(request):
    # movies = Movie.objects.order_by("name")
    # movies = Movie.objects.order_by("-rating")[:5]  # top 5
    # movies = Movie.objects.order_by(F("year").asc(nulls_last=True), 'rating')
    movies = Movie.objects.annotate(
        new_field_bool=Value(True),
        new_budget=F('budget')+100
    )
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count("id"))
    for movie in movies:
        movie.save()
    return render(request, "movie_app/all_movies.html", {
        "movies": movies,
        "agg": agg,
        "total": movies.count()
    })


# def show_one_movie(request, id_movie):
#     # movie = Movie.objects.get(id=id_movie)
#     movie = get_object_or_404(Movie, id=id_movie)
#     return render(request, "movie_app/one_movie.html", {
#         "movie": movie
#     })


def show_one_movie(request, slug_movie: str):
    # movie = Movie.objects.get(id=id_movie)
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, "movie_app/one_movie.html", {
        "movie": movie
    })
