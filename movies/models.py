from django.conf import settings
from django.db import models
from django.utils import timezone


GENRES = [
    ("romance", "Romance"),
    ("comedy", "Comedy"),
    ("action", "Action"),
    ("sci-fi", "Sci-Fi"),
    ("suspense", "Suspense"),
    ("thriller", "Thriller"),
    ("adventure", "Adventure"),
    ("faith-based", "FaithBased"),
]


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    genre = models.CharField(max_length=30, choices=GENRES)
    description = models.TextField()
    poster = models.ImageField(
        upload_to="movies/posters/",
        blank=True,
        null=True,
    )
    trailer_url = models.URLField(blank=True)
    external_link = models.URLField(blank=True)

    is_most_recommended = models.BooleanField(default=False)
    top_position = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="1-5 for Top 5",
    )

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(
        upload_to="actors/",
        blank=True,
        null=True,
    )
    biography = models.TextField(blank=True)
    nationality = models.CharField(max_length=120, blank=True)

    movies = models.ManyToManyField(
        Movie,
        blank=True,
        related_name="actors",
    )

    def __str__(self):
        return self.name


class Clip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(
        upload_to="clips/",
        blank=True,
        null=True,
    )
    video_url = models.URLField(blank=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Advertisement(models.Model):
    title = models.CharField(max_length=180)
    text = models.CharField(max_length=350, blank=True)
    image = models.ImageField(
        upload_to="ads/",
        blank=True,
        null=True,
    )
    link = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        return (
            self.active
            and (
                not self.expires_at
                or self.expires_at >= timezone.now()
            )
        )


class WeeklyVote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    active = models.BooleanField(default=True)

    nominees = models.ManyToManyField(
        Movie,
        blank=True,
        related_name="weekly_votes",
    )

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        n = timezone.now()
        return (
            self.active
            and self.starts_at <= n <= self.ends_at
        )


class WeeklyVoteEntry(models.Model):
    weekly_vote = models.ForeignKey(
        WeeklyVote,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="weekly_entries",
    )
    visitor_key = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["weekly_vote", "visitor_key"],
                name="one_weekly_vote_per_visitor",
            )
        ]


class MovieReaction(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    visitor_key = models.CharField(max_length=128)

    value = models.CharField(
        max_length=10,
        choices=[
            ("like", "Like"),
            ("dislike", "Dislike"),
        ],
    )

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "visitor_key"],
                name="one_movie_reaction_per_visitor",
            )
        ]


class PushSubscription(models.Model):
    endpoint = models.URLField(
        max_length=2000,
        unique=True,
    )
    p256dh = models.TextField()
    auth = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="film_saloon_push_subscriptions",
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Push subscription {self.pk}"
