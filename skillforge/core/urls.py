from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/', views.courses, name='courses'),
 
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('search_results/', views.search_results, name='search_results'),
    path("userlogout/", views.userlogout, name="userlogout"),

]    