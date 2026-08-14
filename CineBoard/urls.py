from django.urls import path
from .views import (
    MovieListView, MovieDetailView, MovieCreateView, 
    MovieUpdateView, MovieDeleteView, AddCommentView, 
    BookVipSeatView, UserRegisterView, UserLoginView, UserLogoutView
)

app_name = 'cineboard'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/add/', MovieCreateView.as_view(), name='movie_add'),
    path('movie/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movie/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('movie/<int:pk>/vip_book/', BookVipSeatView.as_view(), name='vip_book'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
