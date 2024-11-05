from django.urls import path

from BackendTennis.views import ImageListCreateView, PricingListCreateView, TagView, CategoryListCreateView, \
    CategoryRetrieveUpdateDestroyView, EventListCreateView, \
    EventRetrieveUpdateDestroyView, ImageRetrieveUpdateDestroyView, NewsRetrieveUpdateDestroyView, NewsListCreateView, \
    PricingRetrieveUpdateDestroyView, TagRetrieveUpdateDestroyView, SponsorRetrieveUpdateDestroyView, \
    SponsorListCreateView, TrainingListCreateView, TrainingRetrieveUpdateDestroyView, BookingListCreateView, \
    BookingRetrieveUpdateDestroyView, TournamentListCreateView, TournamentRetrieveUpdateDestroyView, \
    TeamMemberListCreateView, TeamMemberRetrieveUpdateDestroyView, ProfessorListCreateView, \
    ProfessorRetrieveUpdateDestroyView, TeamPageListCreateView, TeamPageRetrieveUpdateDestroyView, \
    ClubValueListCreateView, ClubValueRetrieveUpdateDestroyView, AboutPageListCreateView, \
    AboutPageRetrieveUpdateDestroyView, RouteListCreateView, RouteRetrieveUpdateDestroyView, \
    NavigationItemListCreateView, \
    NavigationItemRetrieveUpdateDestroyView, \
    HomePageListCreateView, HomePageRetrieveUpdateDestroyView, RenderListCreateView, RenderRetrieveUpdateDestroyView, \
    PageRenderListCreateView, PageRenderRetrieveUpdateDestroyView, NavigationBarListCreateView, \
    NavigationBarRetrieveUpdateDestroyView, PricingPageListCreateView, PricingPageRetrieveUpdateDestroyView, \
    UpdateNavigationItemsView

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

    path('team_page/', TeamPageListCreateView.as_view(), name='team_page_list_create'),
    path('team_page/<uuid:id>/', TeamPageRetrieveUpdateDestroyView.as_view(),
         name='team_page_retrieve_update_destroy'),

    path('club_value/', ClubValueListCreateView.as_view(), name='club_value_list_create'),
    path('club_value/<uuid:id>/', ClubValueRetrieveUpdateDestroyView.as_view(),
         name='club_value_retrieve_update_destroy'),

    path('about_page/', AboutPageListCreateView.as_view(), name='about_page_list_create'),
    path('about_page/<uuid:id>/', AboutPageRetrieveUpdateDestroyView.as_view(),
         name='about_page_retrieve_update_destroy'),

    path('route/', RouteListCreateView.as_view(), name='route_list_create'),
    path(
        'route/<uuid:id>/',
        RouteRetrieveUpdateDestroyView.as_view(),
        name='route_retrieve_update_destroy'
    ),

    path('navigation_item/', NavigationItemListCreateView.as_view(), name='navigation_item_list_create'),
    path(
        'navigation_item/<uuid:id>/',
        NavigationItemRetrieveUpdateDestroyView.as_view(),
        name='navigation_item_retrieve_update_destroy'
    ),

    path(
        'navigation_items/',
        UpdateNavigationItemsView.as_view(),
        name='navigation_items_update'
    ),

    path('home_page/', HomePageListCreateView.as_view(), name='home_page_list_create'),
    path(
        'home_page/<uuid:id>/',
        HomePageRetrieveUpdateDestroyView.as_view(),
        name='home_page_retrieve_update_destroy'
    ),

    path('render/', RenderListCreateView.as_view(), name='render_list_create'),
    path(
        'render/<uuid:id>/',
        RenderRetrieveUpdateDestroyView.as_view(),
        name='render_retrieve_update_destroy'
    ),

    path('page_render/', PageRenderListCreateView.as_view(), name='page_render_list_create'),
    path(
        'page_render/<uuid:id>/',
        PageRenderRetrieveUpdateDestroyView.as_view(),
        name='page_render_retrieve_update_destroy'
    ),

    path('navigation_bar/', NavigationBarListCreateView.as_view(), name='navigation_bar_list_create'),
    path(
        'navigation_bar/<uuid:id>/',
        NavigationBarRetrieveUpdateDestroyView.as_view(),
        name='navigation_bar_retrieve_update_destroy'
    ),

    path('pricing_page/', PricingPageListCreateView.as_view(), name='pricing_page_list_create'),
    path(
        'pricing_page/<uuid:id>/',
        PricingPageRetrieveUpdateDestroyView.as_view(),
        name='pricing_page_retrieve_update_destroy'
    ),

    # path('admin/users/', UserAdminView.as_view(), name='user-admin'),
    # path('admin/users/<uuid:id>/', UserAdminView.as_view(), name='user-admin-detail'),
    # path('register/', UserRegisterView.as_view(), name='user-register'),

]
