# -*- coding: utf-8 -*-
from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from .utils import set_online, set_offline


# Пользовательский класс обработки websocket
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Вызывается при создании соединения
        await self.accept()

        # Добавить новое подключение к группе
        await self.channel_layer.group_add("chat", self.channel_name)

    # Вызывается при получении
    async def receive_json(self, message):
        # Единое сообщение
        # ожидание self.send_json(content=content)

        # Информационный пакет
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat.message",
                "msg": message.get('msg'),
                "color": message.get('color'),
            },
        )

    # Вызывается, когда соединение закрыто.
    async def disconnect(self, close_code):
        # Удалить закрытое соединение из группы
        await self.channel_layer.group_discard("chat", self.channel_name)

        await self.close()

    async def chat_message(self, event):
        # Обрабатывает событие «chat.message», когда оно отправляется нам.
        await self.send_json({
            "msg": event["msg"],
            "color": event['color'],
        })


class ChatConsumerCrm(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("chat_crm", self.channel_name)

    async def receive_json(self, message):
        await self.channel_layer.group_send(
            "chat_crm",
            {
                "type": "chat.message",
                "msg": message.get('msg'),
                "color": message.get('color'),
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat_crm", self.channel_name)
        await self.close()

    async def chat_message(self, event):
        await self.send_json({
            "msg": event["msg"],
            "color": event['color'],
        })
