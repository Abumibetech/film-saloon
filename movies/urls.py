from django.urls import path
from . import views
urlpatterns=[
 path("",views.home,name="home"),path("genres/",views.genres,name="genres"),path("genres/<slug:slug>/",views.genre_detail,name="genre_detail"),
 path("movie/<slug:slug>/",views.movie_detail,name="movie_detail"),path("movie/<slug:slug>/react/<str:value>/",views.react,name="react"),
 path("vote/<int:vote_id>/<int:movie_id>/",views.cast_vote,name="cast_vote"),path("clips/",views.clips,name="clips"),
 path("actors/",views.actors,name="actors"),path("actors/<slug:slug>/",views.actor_detail,name="actor_detail"),path("search/",views.search,name="search")
]
