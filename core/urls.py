from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    # Website base index views urls
    # home page url
    path('', views.BaseIndexView.as_view(), name="base-index"),
    # wish create, update, detail, delete, list views' urls
    path('wish/create/', views.WishCreateView.as_view(), name="create-wish"),
    path('wish/update/<slug:slug>', views.WishUpdateView.as_view(), name="update-wish"),
    # path('wish/detail/<str:slug>', views.WishDetailView.as_view(), name="detail-wish"),
    path('<slug:slug>', views.WishDetailView.as_view(), name="detail-wish"),
    path('wish/delete/', views.WishDeleteView.as_view(), name="delete-wish"),
    path('wishes/', views.WishesListView.as_view(), name="wishes"),
    # ajax views' urls
    path('wishes-ajax/', views.WishAjaxView.as_view(), name="wishes-ajax"),
    path('subscribe/', views.SubscribeView.as_view(), name="subscribe"),
    # additional pages' urls
    path('coming-soon/', views.ComingSoonView.as_view(), name="coming-soon"),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path('howitworks/', views.HowItWorksView.as_view(), name="howitworks"),
]
