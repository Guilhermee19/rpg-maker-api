import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'dice_{self.room_code}'

        # Entra no grupo (canal)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Sai do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        if not text_data:
            return

        try:
            # Transforma o que veio do front em dicionário Python
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        # Identifica quem enviou (opcional, mas útil para o front saber quem rolou)
        user = self.scope.get('user')
        sender_name = user.username if user and hasattr(user, 'username') and user.is_authenticated else 'Anônimo'
        
        # Adiciona o remetente ao pacote de dados original
        data['sender_username'] = sender_name

        # Manda o objeto INTEIRO (com qualquer action que você inventar no front)
        # para todos os outros membros do grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_handler', # Chama a função abaixo
                'payload': data
            }
        )

    # Função que efetivamente "empurra" a mensagem para os navegadores
    async def broadcast_handler(self, event):
        # Pega o payload que veio do group_send e envia via socket
        await self.send(text_data=json.dumps(event['payload']))