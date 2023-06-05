from django.urls import path

from BackendTennis.views import BookingView, ImageView, SponsorView, PricingView, CategoryView, EventView, NewsView, TagView

app_name = 'BackendTennis'
urlpatterns = [
    path('booking/', BookingView.as_view()),  # GET, POST
    path('booking/<str:id>/', BookingView.as_view()),  # DELETE, GET
    path('booking/<str:id>/update/', BookingView.as_view()),  # PATCH


    path('image/', ImageView.as_view()),  # GET, POST
    path('image/<str:id>/', ImageView.as_view()),  # DELETE, GET
    path('image/<str:id>/update/', ImageView.as_view()),  # PATCH


    path('sponsor/', SponsorView.as_view()),  # GET, POST
    path('sponsor/<str:id>/', SponsorView.as_view()),  # DELETE, GET
    path('sponsor/<str:id>/update/', SponsorView.as_view()),  # PATCH
    
    
    path('pricing/', PricingView.as_view()),  # GET, POST
    path('pricing/<str:id>/', PricingView.as_view()),  # DELETE, GET
    path('pricing/<str:id>/update/', PricingView.as_view()),  # PATCH
    
    
    path('category/', CategoryView.as_view()),  # GET, POST
    path('category/<str:id>/', CategoryView.as_view()),  # DELETE, GET
    path('category/<str:id>/update/', CategoryView.as_view()),  # PATCH
    
    
    path('event/', EventView.as_view()),  # GET, POST
    path('event/<str:id>/', EventView.as_view()),  # DELETE, GET
    path('event/<str:id>/update/', EventView.as_view()),  # PATCH
    
    
    path('news/', NewsView.as_view()),  # GET, POST
    path('news/<str:id>/', NewsView.as_view()),  # DELETE, GET
    path('news/<str:id>/update/', NewsView.as_view()),  # PATCH
    
    
    path('tag/', TagView.as_view()),  # GET, POST
    path('tag/<str:id>/', TagView.as_view()),  # DELETE, GET
    path('tag/<str:id>/update/', TagView.as_view())  # PATCH
    
]
