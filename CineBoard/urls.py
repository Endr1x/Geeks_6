from django.urls import path
from . import views

app_name = 'cineboard'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie/add/', views.MovieCreateView.as_view(), name='movie_add'),
    path('movie/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie_edit'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
    path('movie/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('movie/<int:pk>/vip-book/', views.BookVIPView.as_view(), name='book_vip'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
