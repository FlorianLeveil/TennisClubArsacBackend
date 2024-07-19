from django.urls import path

from BackendTennis.views import ImageView, SponsorView, PricingView, CategoryView, EventView, NewsView, \
    TagView, CategoryListCreateView, CategoryRetrieveUpdateDestroyView, EventListCreateView, \
    EventRetrieveUpdateDestroyView, ImageRetrieveUpdateDestroyView, NewsRetrieveUpdateDestroyView, NewsListCreateView, \
    PricingRetrieveUpdateDestroyView
from BackendTennis.views import BookingListCreateView, BookingRetrieveUpdateDestroyView

app_name = 'BackendTennis'
urlpatterns = [

    path('booking/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('booking/<uuid:id>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_retrieve_update_destroy'),

    path('images/', ImageView.as_view(), name='image-list-create'),
    path('images/<uuid:id>/', ImageRetrieveUpdateDestroyView.as_view(), name='image-retrieve-update-destroy'),

    path('pricing/', PricingView.as_view(), name='pricing-list-create'),
    path('pricing/<uuid:id>/', PricingRetrieveUpdateDestroyView.as_view(), name='pricing-retrieve-update-destroy'),


    path('category/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('category/<uuid:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_update_destroy'),

    path('event/', EventListCreateView.as_view(), name='event_list_create'),
    path('event/<uuid:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event_retrieve_update_destroy'),


    path('news/', NewsListCreateView.as_view(), name='news_list_create'),
    path('news/<uuid:id>/', NewsRetrieveUpdateDestroyView.as_view(), name='news_retrieve_update_destroy'),

    path('tag/', TagView.as_view()),  # GET, POST
    path('tag/<str:id>/', TagView.as_view()),  # DELETE, GET
    path('tag/<str:id>/update/', TagView.as_view())  # PATCH

]
