import types
from typing import List


class Constant(types.SimpleNamespace):
    IMAGE_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        ABOUT_PAGE='about_page',
        ADMIN='admin',
        EVENT='event',
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

    def __setattr__(self, *_):
        raise Exception('Tried to change the value of a constant')


constant_image_type_list: List = list(vars(Constant.IMAGE_TYPE).values())
constant_pricing_type_list: List = list(vars(Constant.PRICING_TYPE).values())
constant_event_mode_list: List = list(vars(Constant.EVENT_MODE).values())
constant_route_protocol_list: List = list(vars(Constant.ROUTE_PROTOCOL_CHOICES).values())
