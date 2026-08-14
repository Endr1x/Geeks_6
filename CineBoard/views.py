from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from .models import Movie, Genre, Comment, VipSeatBooking
from .forms import MovieForm, CommentForm, VipBookingForm, CustomUserRegisterForm

class MovieListView(ListView):
    model = Movie
    template_name = 'CineBoard/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 6

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        genre_id = self.request.GET.get('genre')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['selected_genre'] = self.request.GET.get('genre')
        context['query'] = self.request.GET.get('q', '')
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'CineBoard/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['booking_form'] = VipBookingForm()
        
        user_booking = None
        if self.request.user.is_authenticated:
            user_booking = VipSeatBooking.objects.filter(user=self.request.user, movie=self.object).first()
        context['user_booking'] = user_booking
        return context

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'CineBoard/movie_form.html'
    success_url = reverse_lazy('cineboard:movie_list')

class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'CineBoard/movie_form.html'

    def get_success_url(self):
        return reverse('cineboard:movie_detail', kwargs={'pk': self.object.pk})

class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'CineBoard/movie_confirm_delete.html'
    success_url = reverse_lazy('cineboard:movie_list')

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.movie = movie
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cineboard:movie_detail', kwargs={'pk': self.kwargs['pk']})

class BookVipSeatView(LoginRequiredMixin, CreateView):
    model = VipSeatBooking
    form_class = VipBookingForm

    def form_valid(self, form):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        form.instance.movie = movie
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cineboard:movie_detail', kwargs={'pk': self.kwargs['pk']})

class UserRegisterView(CreateView):
    form_class = CustomUserRegisterForm
    template_name = 'CineBoard/register.html'
    success_url = reverse_lazy('cineboard:login')

class UserLoginView(LoginView):
    template_name = 'CineBoard/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('cineboard:movie_list')
