import types


class MsgHandlerFactory(object):

    def __init__(self, next_handler_factory):
        super(MsgHandlerFactory, self).__init__()
        self.__next_factory = next_handler_factory

    def process(self, xml_content):
        if self.__next_factory:
            return self.__next_factory.process(xml_content)
        else:
            return None


class EventClickHandlerFactory(MsgHandlerFactory):

    def __init__(self, next_handler_factory=None):
        super(EventClickHandlerFactory, self).__init__(next_handler_factory)
        self.__factory = {}

    def put(self, buttonKey, func):
        assert isinstance(func, types.FunctionType)
        self.__factory[buttonKey] = func

    def process(self, xml_content):
        if xml_content['xml']['MsgType'] == 'event' and xml_content['xml']['Event'] == 'click':
            return self.__factory.get(xml_content['xml']['EventKey'], None)
        else:
            return super(EventClickHandlerFactory, self).process(xml_content)


class PoolTextMsgHandlerFactory(MsgHandlerFactory):

    def __init__(self, next_handler_factory=None):
        super(PoolTextMsgHandlerFactory, self).__init__(next_handler_factory)
        self.__factory = {}

    def put(self, text_key, func):
        assert isinstance(func, types.FunctionType)
        self.__factory[text_key] = func

    def process(self, xml_content):
        if xml_content['xml']['MsgType'] == 'text':
            return self.__factory.get(xml_content['xml']['Content'], None)
        else:
            return super(PoolTextMsgHandlerFactory, self).process(xml_content)