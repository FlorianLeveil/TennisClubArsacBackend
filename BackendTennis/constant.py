import types


class Constant(types.SimpleNamespace):
    IMAGE_TYPE: types.SimpleNamespace = types.SimpleNamespace(
        PRICING="pricing",
        NEWS="news",
        EVENTS="event",
        SPONSOR="sponsor",
        PICTURE="picture"
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
