import types
from typing import List


class Constant(types.SimpleNamespace):
    IMAGE_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        ABOUT_PAGE='about_page',
        ADMIN='admin',
        EVENT='event',
        MENU_ITEM='menu_item',
        NEWS='news',
        PICTURE='picture',
        PRICING='pricing',
        PROFESSOR='professor',
        SPONSOR='sponsor',
        TEAM_MEMBER='team_member',
        TEAM_PAGE='team_page',
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

    def __setattr__(self, *_):
        raise Exception('Tried to change the value of a constant')


constant_image_type_list: List = list(vars(Constant.IMAGE_TYPE).values())
constant_pricing_type_list: List = list(vars(Constant.PRICING_TYPE).values())
constant_event_mode_list: List = list(vars(Constant.EVENT_MODE).values())
constant_route_protocol_list: List = list(vars(Constant.ROUTE_PROTOCOL_CHOICES).values())
constant_nav_bar_position_list: List = list(vars(Constant.NAV_BAR_POSITION_CHOICES).values())
constant_render_type_list: List = list(vars(Constant.RENDER_TYPE_CHOICES).values())
