from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Inicializa a aplicação
app = FastAPI(title = "Servidor Ito")

# Classe quem está conectado no jogo
class ConnectionManager:
    def __init__(self):
        # Guarda a conexão dos jogadores
        self.active_connections: list[WebSocket] = []
    
    # Adiciona um jogador à lista de conexões ativas
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    # Remove a conexão de um jogador
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Envia uma mensagem para todos os jogadores conectados
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Rota de teste
@app.get("/")
async def root():
    return{"status": "online", "message": "O servidor do Ito está rodando"}

# Rota do WebSocket para os jogadores se conectarem
@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await manager.connect(websocket)
    await manager.broadcast(f"{player_name} entrou no jogo")

    try:
        # Fica escutando qualquer ação do jogador infinitamente
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{player_name}: {data}")
        
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{player_name} saiu do jogo")