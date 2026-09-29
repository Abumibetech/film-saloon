from django.contrib import admin
from .models import Movie,Actor,Clip,Advertisement,WeeklyVote,WeeklyVoteEntry,MovieReaction
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=("title","genre","is_most_recommended","top_position","likes","dislikes","views")
    list_filter=("genre","is_most_recommended"); search_fields=("title","description"); prepopulated_fields={"slug":("title",)}; list_editable=("is_most_recommended","top_position")
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display=("name","nationality"); search_fields=("name","biography"); prepopulated_fields={"slug":("name",)}; filter_horizontal=("movies",)
@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin): list_display=("title","created_at"); search_fields=("title","description")
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin): list_display=("title","active","expires_at"); list_filter=("active",)
@admin.register(WeeklyVote)
class WeeklyVoteAdmin(admin.ModelAdmin): list_display=("title","starts_at","ends_at","active"); list_filter=("active",); filter_horizontal=("nominees",)
@admin.register(WeeklyVoteEntry)
class WeeklyVoteEntryAdmin(admin.ModelAdmin): list_display=("weekly_vote","movie","visitor_key","created_at"); readonly_fields=("weekly_vote","movie","visitor_key","created_at")
@admin.register(MovieReaction)
class MovieReactionAdmin(admin.ModelAdmin): list_display=("movie","visitor_key","value","created_at"); readonly_fields=("movie","visitor_key","value","created_at")
admin.site.site_header="FILM SALOON"; admin.site.site_title="FILM SALOON"; admin.site.index_title="Content Management"
