from django.contrib import admin
from django import forms

from .models import (
    Genre,
    Movie,
    Actor,
    Clip,
    Advertisement,
    WeeklyVote,
    WeeklyVoteEntry,
    MovieReaction,
    PushSubscription,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "active")
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "genre" in self.fields:
            active_genres = Genre.objects.filter(
                active=True
            ).order_by("order", "name")

            choices = [
                ("", "---------"),
            ]

            choices.extend(
                (genre.slug, genre.name)
                for genre in active_genres
            )

            # Preserve an existing movie's genre even if that genre
            # has been deactivated in Genre Admin.
            current_value = self.instance.genre

            if current_value and not any(
                value == current_value
                for value, label in choices
            ):
                choices.append(
                    (
                        current_value,
                        f"{current_value} (inactive)"
                    )
                )

            self.fields["genre"].choices = choices


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = (
        "title",
        "genre",
        "is_most_recommended",
        "top_position",
        "likes",
        "dislikes",
        "views",
    )

    list_filter = (
        "genre",
        "is_most_recommended",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "is_most_recommended",
        "top_position",
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nationality",
    )

    search_fields = (
        "name",
        "biography",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    filter_horizontal = (
        "movies",
    )


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "active",
        "expires_at",
    )

    list_filter = (
        "active",
    )


@admin.register(WeeklyVote)
class WeeklyVoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "starts_at",
        "ends_at",
        "active",
    )

    list_filter = (
        "active",
    )

    filter_horizontal = (
        "nominees",
    )


@admin.register(WeeklyVoteEntry)
class WeeklyVoteEntryAdmin(admin.ModelAdmin):
    list_display = (
        "weekly_vote",
        "movie",
        "visitor_key",
        "created_at",
    )

    readonly_fields = (
        "weekly_vote",
        "movie",
        "visitor_key",
        "created_at",
    )


@admin.register(MovieReaction)
class MovieReactionAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "visitor_key",
        "value",
        "created_at",
    )

    readonly_fields = (
        "movie",
        "visitor_key",
        "value",
        "created_at",
    )


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "endpoint",
    )

    readonly_fields = (
        "endpoint",
        "p256dh",
        "auth",
        "user",
        "created_at",
        "updated_at",
    )


admin.site.site_header = "FILM SALOON"
admin.site.site_title = "FILM SALOON"
admin.site.index_title = "Content Management"
