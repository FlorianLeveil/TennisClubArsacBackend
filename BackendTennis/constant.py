import types
from typing import List


class Constant(types.SimpleNamespace):
    IMAGE_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        PRICING="pricing",
        NEWS="news",
        EVENTS="event",
        SPONSOR="sponsor",
        PICTURE="picture",
        ADMIN="admin"
    )

    PRICING_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        OTHER="other",
        CHILDREN="children",
        ADULT="adult"
    )

    EVENT_MODE: types.SimpleNamespace = types.SimpleNamespace(
        HISTORY="history",
        FUTURE_EVENT="future_event"
    )

    def __setattr__(self, *_):
        raise Exception("Tried to change the value of a constant")


constant_image_type_list: List = list(vars(Constant.IMAGE_TYPE).values())
constant_pricing_type_list: List = list(vars(Constant.PRICING_TYPE).values())
constant_event_mode_list: List = list(vars(Constant.EVENT_MODE).values())
