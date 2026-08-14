from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Movie, Genre, Comment, VIPBooking
from .forms import MovieForm, CommentForm, VIPBookingForm


class MovieListView(ListView):
    model = Movie
    template_name = 'cineboard/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('genres')
        search_query = self.request.GET.get('q')
        genre_id = self.request.GET.get('genre')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'cineboard/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['vip_form'] = VIPBookingForm()
        if self.request.user.is_authenticated:
            context['user_vip_booking'] = VIPBooking.objects.filter(user=self.request.user).first()
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'cineboard/movie_form.html'
    success_url = reverse_lazy('cineboard:movie_list')


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'cineboard/movie_form.html'

    def get_success_url(self):
        return reverse('cineboard:movie_detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'cineboard/movie_confirm_delete.html'
    success_url = reverse_lazy('cineboard:movie_list')


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.movie = movie
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, "Комментарий добавлен!")
        return redirect('cineboard:movie_detail', pk=movie.pk)


class BookVIPView(LoginRequiredMixin, CreateView):
    model = VIPBooking
    form_class = VIPBookingForm

    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        if VIPBooking.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "Вы уже забронировали 1 VIP-место!")
            return redirect('cineboard:movie_detail', pk=movie.pk)

        form.instance.user = self.request.user
        form.instance.movie = movie
        form.save()
        messages.success(self.request, f"VIP место №{form.instance.seat_number} забронировано!")
        return redirect('cineboard:movie_detail', pk=movie.pk)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
