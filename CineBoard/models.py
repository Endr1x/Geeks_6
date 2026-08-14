from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра", unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание фильма", default="")
    release_year = models.PositiveIntegerField(verbose_name="Год выпуска", default=2024)
    director = models.CharField(max_length=255, verbose_name="Режиссер", default="Не указан")
    country = models.CharField(max_length=100, verbose_name="Страна", default="Не указана")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (в мин)", default=120)
    age_rating = models.CharField(max_length=10, verbose_name="Возрастной рейтинг", default="16+")
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="Рейтинг (0-10)"
    )
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True, verbose_name="Постер")
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name="Жанры")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class VIPBooking(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vip_booking',
        verbose_name="Пользователь"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='vip_bookings', verbose_name="Фильм")
    seat_number = models.PositiveIntegerField(verbose_name="Номер VIP места")
    booked_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    class Meta:
        verbose_name = "VIP Бронирование"
        verbose_name_plural = "VIP Бронирования"

    def __str__(self):
        return f"VIP место {self.seat_number} - {self.user} ({self.movie.title})"


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments', verbose_name="Фильм")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        return f"Коммент от {self.author} к {self.movie.title}"
