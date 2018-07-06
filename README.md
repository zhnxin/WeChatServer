# weChatServer

## request
- python 2.7/3.x
- tornado
- xmltodict

## introduction
- 支持同企业多企业号配置
- 支持access_token自动更新
- 支持通过token主动发送消息
- 支持企业号事件(文本消息，菜单点击事件)处理

## PS
- 自带demo为点击事件自动回复
- 自带demo用户回复文本，回复图片/文本

## 消息回复Usage

### handler

"""
def defaultHandler(xml_contend, sMsgCrypt):
    textSend = PassiveTextMsg(xml_contend)
    msg = 'hello world!'
    to_xml = textSend.generate(msg=msg)
return to_xml
"""
传入已经解密的消息和加密类实例，返回构造完毕的回复消息str xml

### 责任链模式

"""
textHandlerFactory = PoolTextMsgHandlerFactory()
clickHandlerFactory = EventClickHandlerFactory(textHandlerFactory)

# handler factory 入口
def getHandler(xml_content):
    global clickHandlerFactory
return clickHandlerFactory.process(xml_content)
"""

### PoolTextMsgHandlerFactory

简陋的文本消息响应handlerFactory，通过匹配用户输入的utf-8文本返回hander回调方法。

"""
# textHandlerFactory.put(u'<key word>',callbackHandler)
textHandlerFactory.put(u"颜文字", defaultHandler)
textHandlerFactory.put(u'溜了溜了', enentHandlerDemo_image)
"""
  
### EventClickHandlerFactory

点击事件响应handlerFactory，通过匹配用户点击的菜单id，返回对应回调方法
"""
#clickHandlerFactory.put('<menu id>',callbackHandler)
clickHandlerFactory.put('10001', eventHandlerDemo)
clickHandlerFactory.put('10002', enentHandlerDemo_image)
"""
