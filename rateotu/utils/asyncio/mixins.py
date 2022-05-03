import json

from django.core.serializers.json import DjangoJSONEncoder


class AsyncJsonEncoderDecoderMixin:
    """
    Mixin that automatically JSON-encodes and decodes messages as they come
    in and go out. Expects everything to be text; will error on binary data.
    Also, useful when serializing Decimal, datetime, timedelta, UUID to JSON.
    """

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            await self.receive_json(await self.decode_json(text_data), **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    async def receive_json(self, content, **kwargs):
        """
        Called with decoded JSON content.
        """
        pass

    async def send_json(self, content, close=False):
        """
        Encode the given content as JSON and send it to the client.
        """
        await super().send(text_data=await self.encode_json(content), close=close)

    @classmethod
    async def decode_json(cls, text_data):
        return json.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, cls=DjangoJSONEncoder)
