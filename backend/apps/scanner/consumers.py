from channels.generic.websocket import AsyncJsonWebsocketConsumer
class ScannerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self): await self.channel_layer.group_add('scanner',self.channel_name); await self.accept()
    async def disconnect(self,code): await self.channel_layer.group_discard('scanner',self.channel_name)
    async def scanner_event(self,event): await self.send_json(event['data'])
