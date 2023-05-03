class Constant(object):
    IMAGE_TAG = {}
    IMAGE_TAG.PRICING = "PICING"
    IMAGE_TAG.NEWS = "NEWS"
    IMAGE_TAG.EVENTS = "EVENT"
    IMAGE_TAG.SPONSOR = "SPONSOR"


    def __setattr__(self, *_):
        raise Exception("Tried to change the value of a constant")