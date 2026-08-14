from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Жанр")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Постер/Фото")
    release_date = models.DateField(verbose_name="Дата выхода")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    country = models.CharField(max_length=100, verbose_name="Страна")
    director = models.CharField(max_length=150, verbose_name="Режиссер")
    age_limit = models.CharField(max_length=10, default="16+", verbose_name="Возрастное ограничение")
    vip_price = models.DecimalField(max_digits=10, decimal_places=2, default=500.00, verbose_name="Цена VIP билета")
    genres = models.ManyToManyField(Genre, related_name="movies", verbose_name="Жанры")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments", verbose_name="Фильм")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return f"{self.author} - {self.movie.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class VipSeatBooking(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="vip_bookings", verbose_name="Фильм")
    seat_number = models.PositiveIntegerField(verbose_name="Номер VIP места")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} (Место {self.seat_number})"

    class Meta:
        verbose_name = "VIP Бронирование"
        verbose_name_plural = "VIP Бронирования"
