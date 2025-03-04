from __future__ import annotations

import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


class Constant(types.SimpleNamespace):
    IMAGE_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        ABOUT_PAGE='about_page',
        ADMIN='admin',
        EVENT='event',
        NAVIGATION_BAR='navigation_bar',
        NAVIGATION_ITEM='navigation_item',
        NEWS='news',
        PICTURE='picture',
        PRICING='pricing',
        PROFESSOR='professor',
        SPONSOR='sponsor',
        TEAM_MEMBER='team_member',
        TEAM_PAGE='team_page',
    )

    IMAGE_TYPE_TRAD = types.SimpleNamespace(
        ABOUT_PAGE={'key': 'about_page', 'label': {'en': 'About Page', 'fr': 'Page À Propos'}},
        ADMIN={'key': 'admin', 'label': {'en': 'Admin', 'fr': 'Administration'}},
        EVENT={'key': 'event', 'label': {'en': 'Event', 'fr': 'Événement'}},
        NAVIGATION_BAR={'key': 'navigation_bar', 'label': {'en': 'Navigation Bar', 'fr': 'Barre de Navigation'}},
        NAVIGATION_ITEM={'key': 'navigation_item', 'label': {'en': 'Home Page', 'fr': 'Page Accueil'}},
        NEWS={'key': 'news', 'label': {'en': 'News', 'fr': 'Actualités'}},
        PICTURE={'key': 'picture', 'label': {'en': 'Picture', 'fr': 'Image'}},
        PRICING={'key': 'pricing', 'label': {'en': 'Pricing', 'fr': 'Tarifs'}},
        PROFESSOR={'key': 'professor', 'label': {'en': 'Professor', 'fr': 'Professeur'}},
        SPONSOR={'key': 'sponsor', 'label': {'en': 'Sponsor', 'fr': 'Sponsor'}},
        TEAM_MEMBER={'key': 'team_member', 'label': {'en': 'Team Member', 'fr': 'Membre de l\'Équipe'}},
        TEAM_PAGE={'key': 'team_page', 'label': {'en': 'Team Page', 'fr': 'Page d\'Équipe'}}
    )

    PRICING_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        OTHER='other',
        CHILDREN='children',
        ADULT='adult'
    )

    EVENT_MODE: types.SimpleNamespace = types.SimpleNamespace(
        HISTORY='history',
        FUTURE_EVENT='future_event'
    )

    ROUTE_PROTOCOL_CHOICES: types.SimpleNamespace = types.SimpleNamespace(
        HTTP=('http', 'HTTP'),
        HTTPS=('https', 'HTTPS')
    )

    NAV_BAR_POSITION_CHOICES: types.SimpleNamespace = types.SimpleNamespace(
        LEFT=('left', 'LEFT'),
        CENTER=('center', 'CENTER'),
        RIGHT=('right', 'RIGHT')
    )

    RENDER_TYPE_CHOICES: types.SimpleNamespace = types.SimpleNamespace(
        NAV_BAR=('nav_bar', 'NAV_BAR'),
        HOME_PAGE=('home_page', 'HOME_PAGE'),
    )
    FORM_INPUT_NAME_CHOICES: types.SimpleNamespace = types.SimpleNamespace(
        FIRSTNAME=('firstname', 'prénom'),
        LASTNAME=('lastname', 'nom'),
        PHONE_NUMBER=('phone_number', 'numéro de téléphone'),
        MAIL=('mail', 'email'),
        SUBJECT=('subject', 'sujet'),
        MESSAGE=('message', 'message')
    )

    def __setattr__(self, *_):
        raise Exception('Tried to change the value of a constant')


constant_image_type_list: List = list(vars(Constant.IMAGE_TYPE).values())
constant_pricing_type_list: List = list(vars(Constant.PRICING_TYPE).values())
constant_event_mode_list: List = list(vars(Constant.EVENT_MODE).values())
constant_route_protocol_list: List = list(vars(Constant.ROUTE_PROTOCOL_CHOICES).values())
constant_nav_bar_position_list: List = list(vars(Constant.NAV_BAR_POSITION_CHOICES).values())
constant_render_type_list: List = list(vars(Constant.RENDER_TYPE_CHOICES).values())
constant_form_input_name: List = list(vars(Constant.FORM_INPUT_NAME_CHOICES).values())
