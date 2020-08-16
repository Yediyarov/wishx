from django.urls import path, reverse_lazy
from base_user import views
from django.contrib.auth import (views as auth_views)

app_name = 'account'

urlpatterns = [
    # Authentication Login Register urls here

    # Account Login urls here
    path('login/', views.AccountBaseLoginView.as_view(), name="login"),

    # Account Register urls here
    path('register/', views.AccountRegistrationView.as_view(), name="register"),
    path('register/done', views.AccountRegistrationDoneView.as_view(), name="register-done"),
    path('register/<uidb64>/<token>/', views.AccountRegistrationConfirmView.as_view(), name='register-confirm'),

    # Base Logout views url here
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('core:base-index')), name="logout"),

    # Account forget password url here
    path('forget/', views.ForgetPasswordView.as_view(), name="forget"),
    path('forget/done', views.ForgetPasswordDoneView.as_view(), name="forget-done"),
    path('forget/<uidb64>/<token>/', views.ForgetPasswordResetConfirmView.as_view(), name="forget-reset-confirm"),

    # Account edit view url here
    path('edit/', views.AccountEditView.as_view(), name="account-edit"),

    # Account detail view url here
    path('detail/<str:slug>/', views.AccountDetailView.as_view(), name='account-detail'),

    # Account update view url here
    path('update/', views.AccountUpdateView.as_view(), name="account-update")

]
