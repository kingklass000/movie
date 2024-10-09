from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    STATUS_CHOICES = (
        ('pro', 'Pro'),
        ('simple', 'Simple'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=100)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=100)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='movies', on_delete=models.CASCADE)
    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, related_name='movies')
    genre = models.ForeignKey(Genre, related_name='movies', on_delete=models.CASCADE)

    TYPES = (
        (144, '144p'),
        (360, '360p'),
        (480, '480p'),
        (720, '720p'),
        (1080, '1080p'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPES)
    movie_time = models.DurationField()
    description = models.TextField()
    movie_trailer = models.FileField(verbose_name='видео', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_images/')
    STATUS_CHOICES = (
        ('pro', 'Pro'),
        ('simple', 'Simple'),
    )
    status_movie = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.movie_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class MovieLanguage(models.Model):
    language = models.CharField(max_length=100)
    video = models.FileField(verbose_name='видео', null=True, blank=True)
    movie = models.ForeignKey(Movie, related_name='languages', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language} - {self.movie}'


class Moment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
    movie_moment = models.FileField(verbose_name='видео', null=True, blank=True)

    def __str__(self):
        return f'Moment from {self.movie}'


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], verbose_name='Рейтинг')
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movie} - {self.user} - {self.stars} stars'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} favorites'


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, related_name='items', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cart} - {self.movie}'


class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='history', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed {self.movie} at {self.viewed_at}'