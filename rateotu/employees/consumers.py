from channels.generic.websocket import AsyncWebsocketConsumer

from rateotu.utils.asyncio.mixins import AsyncJsonEncoderDecoderMixin
from rateotu.utils.asyncio.selectors import get_employee_role


class EmployeeNotificationConsumer(
    AsyncJsonEncoderDecoderMixin, AsyncWebsocketConsumer
):
    """
    Receives and broadcasts real-time data to all connected employees (WS clients).
    """

    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = None

        # Check if a user is authenticated trough JWT (SEE: utils/websocket/auth)
        if not self.user.is_authenticated:
            return await self.close()
        # Check permissions
        if not self.user.is_employee:
            return await self.close()

        # Crate the group name
        self.group_name = f"ws_employee_{await get_employee_role(self.user)}s"
        # Add channel to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        # Accept connection as the last action in connect()
        await self.accept()

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive a message from the group and broadcast to all connected channels
    # (channels = different employees => one or many client pages, browser tabs,
    # browser windows; client devices, etc).
    async def broadcast_to_employees(self, event):
        """
        Called internally to send a message to a connected employee.
        """
        # Send JSON encoded message to employee
        await self.send_json(event)
