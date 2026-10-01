import hashlib
from django.contrib import messages
from django.db import models,transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from .models import Movie,Actor,Clip,Advertisement,WeeklyVote,WeeklyVoteEntry,MovieReaction,GENRES

def visitor_key(request):
    if not request.session.session_key: request.session.create()
    return hashlib.sha256(request.session.session_key.encode()).hexdigest()

def home(request):
    most=Movie.objects.filter(is_most_recommended=True)[:12]
    top=Movie.objects.filter(top_position__in=[1,2,3,4,5]).order_by("top_position")[:5]
    excluded=set(most.values_list("pk",flat=True))|set(top.values_list("pk",flat=True))
    other=Movie.objects.exclude(pk__in=excluded)[:12]
    vote=WeeklyVote.objects.filter(active=True,starts_at__lte=timezone.now(),ends_at__gte=timezone.now()).order_by("-starts_at").first()
    ads=[a for a in Advertisement.objects.all() if a.is_live][:4]
    return render(request,"movies/home.html",{"most":most,"top":top,"other":other,"active_vote":vote,"nominations":vote.nominees.all() if vote else [],"active_ads":ads,"genres":GENRES})

def genres(request): return render(request,"movies/genres.html",{"genres":GENRES})
def genre_detail(request,slug):
    return render(request,"movies/genre_detail.html",{"genre_name":dict(GENRES).get(slug,slug.replace("-"," ").title()),"movies":Movie.objects.filter(genre=slug)})

def movie_detail(request,slug):
    movie=get_object_or_404(Movie,slug=slug)
    if not request.session.get(f"viewed_{movie.pk}"):
        Movie.objects.filter(pk=movie.pk).update(views=models.F("views")+1); request.session[f"viewed_{movie.pk}"]=True; movie.refresh_from_db()
    return render(request,"movies/movie_detail.html",{"movie":movie,"reaction":MovieReaction.objects.filter(movie=movie,visitor_key=visitor_key(request)).first(),"related":Movie.objects.filter(genre=movie.genre).exclude(pk=movie.pk)[:8]})

def react(request,slug,value):
    movie=get_object_or_404(Movie,slug=slug)
    if request.method!="POST" or value not in ("like","dislike"): return redirect("movie_detail",slug=slug)
    key=visitor_key(request)
    with transaction.atomic():
        old=MovieReaction.objects.filter(movie=movie,visitor_key=key).first()
        if old and old.value==value:
            old.delete()
            Movie.objects.filter(pk=movie.pk).update(**{value+"s":models.F(value+"s")-1})
        elif old:
            other="dislike" if value=="like" else "like"
            old.value=value; old.save(update_fields=["value","created_at"])
            Movie.objects.filter(pk=movie.pk).update(**{value+"s":models.F(value+"s")+1,other+"s":models.F(other+"s")-1})
        else:
            MovieReaction.objects.create(movie=movie,visitor_key=key,value=value)
            Movie.objects.filter(pk=movie.pk).update(**{value+"s":models.F(value+"s")+1})
    return redirect("movie_detail",slug=slug)

def cast_vote(request,vote_id,movie_id):
    vote=get_object_or_404(WeeklyVote,pk=vote_id); movie=get_object_or_404(Movie,pk=movie_id)
    if request.method!="POST" or not vote.is_live or not vote.nominees.filter(pk=movie.pk).exists(): return redirect("home")
    try:
        WeeklyVoteEntry.objects.create(weekly_vote=vote,movie=movie,visitor_key=visitor_key(request))
        messages.success(request,f"Your vote for {movie.title} has been recorded.")
    except Exception: messages.info(request,"You have already voted in this weekly vote.")
    return redirect("home")

def clips(request): return render(request,"movies/clips.html",{"clips":Clip.objects.all()[:40]})
def actors(request):
    q=request.GET.get("q","").strip(); qs=Actor.objects.all()
    if q: qs=qs.filter(Q(name__icontains=q)|Q(biography__icontains=q)|Q(nationality__icontains=q))
    return render(request,"movies/actors.html",{"actors":qs,"query":q})
def actor_detail(request,slug): return render(request,"movies/actor_detail.html",{"actor":get_object_or_404(Actor,slug=slug)})
def search(request):
    q=request.GET.get("q","").strip()
    movies=Movie.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)) if q else Movie.objects.none()
    actors=Actor.objects.filter(Q(name__icontains=q)|Q(biography__icontains=q)) if q else Actor.objects.none()
    return render(request,"movies/search.html",{"query":q,"movies":movies,"actors":actors})
