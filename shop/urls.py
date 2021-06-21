from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView,\
    PasswordResetDoneView,PasswordResetConfirmView,\
    PasswordResetCompleteView
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='shophome'),
    path('about', views.about, name='about_us'),
    path('contect', views.contect, name='contect_us'),
    path('tracker', views.track, name='track_us'),
    path('productview/<int:myid>', views.product_fn, name='products'),
    path('productview/rate/<int:prod_id>', views.Rate, name='rate-product'),
    path('cheakout', views.cheakout, name='cheakout'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('search', views.search, name="search"),
    path('category/<str:catid>/', views.category, name="category"),
    path("password-reset/", PasswordResetView.as_view(template_name='password/password_reset.html'),
         name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name="password_reset_complete"),
]
