"""本模块定义事件响应器便携定义函数。"""

def on_message(self):
    """注册一个消息事件响应器"""
    return self.context["post_type"] == "message"