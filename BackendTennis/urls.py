from django.urls import path

from BackendTennis.views import ImageView, SponsorView, PricingView, CategoryView, EventView, NewsView, \
    TagView, CategoryListCreateView, CategoryRetrieveUpdateDestroyView, EventListCreateView, \
    EventRetrieveUpdateDestroyView, ImageRetrieveUpdateDestroyView
from BackendTennis.views import BookingListCreateView, BookingRetrieveUpdateDestroyView

app_name = 'BackendTennis'
urlpatterns = [

    path('booking/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('booking/<uuid:id>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_retrieve_update_destroy'),

    path('images/', ImageView.as_view(), name='image-list-create'),
    path('images/<uuid:id>/', ImageRetrieveUpdateDestroyView.as_view(), name='image-retrieve-update-destroy'),


    path('sponsor/', SponsorView.as_view()),  # GET, POST
    path('sponsor/<str:id>/', SponsorView.as_view()),  # DELETE, GET
    path('sponsor/<str:id>/update/', SponsorView.as_view()),  # PATCH

    path('pricing/', PricingView.as_view()),  # GET, POST
    path('pricing/<str:id>/', PricingView.as_view()),  # DELETE, GET
    path('pricing/<str:id>/update/', PricingView.as_view()),  # PATCH

    path('category/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('category/<uuid:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_update_destroy'),

    path('event/', EventListCreateView.as_view(), name='event_list_create'),
    path('event/<uuid:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event_retrieve_update_destroy'),


    path('news/', NewsView.as_view()),  # GET, POST
    path('news/<str:id>/', NewsView.as_view()),  # DELETE, GET
    path('news/<str:id>/update/', NewsView.as_view()),  # PATCH

    path('tag/', TagView.as_view()),  # GET, POST
    path('tag/<str:id>/', TagView.as_view()),  # DELETE, GET
    path('tag/<str:id>/update/', TagView.as_view())  # PATCH

]
