from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from movies.models import Movie,WeeklyVote
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        data=[("Love Alive","romance","A heartfelt story about love and second chances."),("Laugh Out Loud","comedy","A fast moving comedy full of memorable moments."),("Final Mission","action","One impossible mission changes everything."),("Beyond Tomorrow","sci-fi","A futuristic journey beyond the expected."),("The Last Clue","suspense","A mystery gets closer to its hidden truth."),("Shadow Chase","thriller","A tense chase through a city of secrets."),("Wild Horizon","adventure","An unforgettable journey beyond familiar territory."),("Faith & Hope","faith-based","A story of family, courage, faith and hope.")]
        for i,(title,genre,desc) in enumerate(data,1):
            Movie.objects.get_or_create(slug=slugify(title),defaults={"title":title,"genre":genre,"description":desc,"top_position":i if i<=5 else None,"is_most_recommended":i<=3})
        vote,_=WeeklyVote.objects.get_or_create(title="Film Saloon Weekly Favorite",defaults={"description":"Choose this week's favorite movie.","starts_at":timezone.now(),"ends_at":timezone.now()+timedelta(days=7),"active":True})
        if vote.nominees.count()==0: vote.nominees.set(Movie.objects.order_by("?")[:4])
        self.stdout.write(self.style.SUCCESS("Starter content is ready."))
