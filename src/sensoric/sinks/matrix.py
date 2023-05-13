"""
A sink that logs to an InfluxDB.
"""
import asyncio

from sensoric.sinks import Sink
from nio import AsyncClient


class NotificationSink(Sink):

    def __init__(self, homeserver: str, user_id: str, access_token: str, room_id: str, msg_template: str):
        self.homeserver = homeserver
        self.user_id = user_id
        self.access_token = access_token
        self.room_id = room_id
        self.msg_template = msg_template

    async def _send_matrix_message(self, message):
        """
        Sends the given message to the given matrix server.
        """
        client = AsyncClient(self.homeserver)
        client.access_token = self.access_token
        client.user_id = self.user_id

        await client.room_send(
            self.room_id,
            message_type='m.room.message',
            content={
                'msgtype': 'm.text',
                'body': message
            })
        await client.close()

    def write_points(self, data):
        asyncio.get_event_loop().run_until_complete(
            self._send_matrix_message(message=self.msg_template.format(data))
        )
