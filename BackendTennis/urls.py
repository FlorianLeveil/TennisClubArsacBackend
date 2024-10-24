from django.urls import path

from BackendTennis.views import ImageListCreateView, PricingListCreateView, TagView, CategoryListCreateView, \
    CategoryRetrieveUpdateDestroyView, EventListCreateView, \
    EventRetrieveUpdateDestroyView, ImageRetrieveUpdateDestroyView, NewsRetrieveUpdateDestroyView, NewsListCreateView, \
    PricingRetrieveUpdateDestroyView, TagRetrieveUpdateDestroyView, SponsorRetrieveUpdateDestroyView, \
    SponsorListCreateView, TrainingListCreateView, TrainingRetrieveUpdateDestroyView, BookingListCreateView, \
    BookingRetrieveUpdateDestroyView, TournamentListCreateView, TournamentRetrieveUpdateDestroyView, \
    TeamMemberListCreateView, TeamMemberRetrieveUpdateDestroyView, ProfessorListCreateView, \
    ProfessorRetrieveUpdateDestroyView

app_name = 'BackendTennis'
urlpatterns = [

    path('booking/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('booking/<uuid:id>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_retrieve_update_destroy'),

    path('image/', ImageListCreateView.as_view(), name='image-list-create'),
    path('image/<uuid:id>/', ImageRetrieveUpdateDestroyView.as_view(), name='image-retrieve-update-destroy'),

    path('pricing/', PricingListCreateView.as_view(), name='pricing-list-create'),
    path('pricing/<uuid:id>/', PricingRetrieveUpdateDestroyView.as_view(), name='pricing-retrieve-update-destroy'),

    path('category/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('category/<uuid:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_update_destroy'),

    path('event/', EventListCreateView.as_view(), name='event_list_create'),
    path('event/<uuid:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event_retrieve_update_destroy'),

    path('news/', NewsListCreateView.as_view(), name='news_list_create'),
    path('news/<uuid:id>/', NewsRetrieveUpdateDestroyView.as_view(), name='news_retrieve_update_destroy'),

    path('tag/', TagView.as_view(), name='tag-list-create'),
    path('tag/<uuid:id>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update-destroy'),

    path('sponsor/', SponsorListCreateView.as_view(), name='sponsor-list-create'),
    path('sponsor/<uuid:id>/', SponsorRetrieveUpdateDestroyView.as_view(), name='sponsor-retrieve-update-destroy'),

    path('training/', TrainingListCreateView.as_view(), name='training_list_create'),
    path('training/<uuid:id>/', TrainingRetrieveUpdateDestroyView.as_view(), name='training_retrieve_update_destroy'),

    path('tournament/', TournamentListCreateView.as_view(), name='tournament_list_create'),
    path('tournament/<uuid:id>/', TournamentRetrieveUpdateDestroyView.as_view(),
         name='tournament_retrieve_update_destroy'),

    path('team_member/', TeamMemberListCreateView.as_view(), name='team_member_list_create'),
    path('team_member/<uuid:id>/', TeamMemberRetrieveUpdateDestroyView.as_view(),
         name='team_member_retrieve_update_destroy'),

    path('professor/', ProfessorListCreateView.as_view(), name='professor_list_create'),
    path('professor/<uuid:id>/', ProfessorRetrieveUpdateDestroyView.as_view(),
         name='professor_retrieve_update_destroy'),

    # path('admin/users/', UserAdminView.as_view(), name='user-admin'),
    # path('admin/users/<uuid:id>/', UserAdminView.as_view(), name='user-admin-detail'),
    # path('register/', UserRegisterView.as_view(), name='user-register'),

]
