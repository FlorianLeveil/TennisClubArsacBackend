from django.urls import path

from BackendTennis.views import BookingView, ImageView, SponsorView

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
    path('sponsor/<str:id>/update/', SponsorView.as_view())  # PATCH
]
