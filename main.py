import random
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# In-memory storage for session text content
storage: Dict[str, str] = {}

class ConnectionManager:
    def __init__(self):
        # Maps session_id to a list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, message: str, session_id: str, exclude: WebSocket = None):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                if connection != exclude:
                    await connection.send_text(message)

manager = ConnectionManager()

def generate_session_id() -> str:
    adjectives = ["shiny", "fast", "blue", "happy", "quiet", "brave", "clever", "wild", "gentle", "lucky"]
    nouns = ["fox", "wolf", "bear", "eagle", "lion", "tiger", "owl", "deer", "shark", "whale"]
    return f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(100, 999)}"

@app.get("/")
async def root():
    return RedirectResponse(url=f"/pastebucket/{generate_session_id()}")

@app.get("/pastebucket/{session_id}", response_class=HTMLResponse)
async def get_pastebucket(session_id: str):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pastebucket - """ + session_id + """</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #f8f9fa;
            }
            .container {
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            .header {
                padding: 10px 20px;
                background-color: #343a40;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.9rem;
            }
            .header span { opacity: 0.8; }
            .header strong { color: #00d1b2; }
            textarea {
                flex-grow: 1;
                border: none;
                padding: 20px;
                font-size: 1.1rem;
                font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
                resize: none;
                outline: none;
                background-color: white;
                line-height: 1.5;
            }
            .status {
                font-size: 0.8rem;
                padding: 2px 8px;
                border-radius: 4px;
            }
            .connected { color: #48c774; }
            .disconnected { color: #f14668; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>Pastebucket: <strong>""" + session_id + """</strong></div>
                <div id="status" class="status connected">Connected</div>
            </div>
            <textarea id="text" placeholder="Start typing or paste something here..."></textarea>
        </div>
        <script>
            const sessionId = '""" + session_id + """';
            const textarea = document.getElementById('text');
            const status = document.getElementById('status');
            
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const socketUrl = `${protocol}//${window.location.host}/ws/${sessionId}`;
            
            let socket;
            let debounceTimer;

            function connect() {
                socket = new WebSocket(socketUrl);

                socket.onopen = () => {
                    status.innerText = 'Connected';
                    status.className = 'status connected';
                };

                socket.onmessage = (event) => {
                    if (textarea.value !== event.data) {
                        const start = textarea.selectionStart;
                        const end = textarea.selectionEnd;
                        textarea.value = event.data;
                        // Attempt to preserve cursor position
                        textarea.setSelectionRange(start, end);
                    }
                };

                socket.onclose = () => {
                    status.innerText = 'Disconnected - Reconnecting...';
                    status.className = 'status disconnected';
                    setTimeout(connect, 2000);
                };

                socket.onerror = (error) => {
                    console.error('WebSocket Error:', error);
                };
            }

            textarea.addEventListener('input', () => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    if (socket.readyState === WebSocket.OPEN) {
                        socket.send(textarea.value);
                    }
                }, 200);
            });

            connect();
        </script>
    </body>
    </html>
    """

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    
    # Send current content to the new connection
    current_content = storage.get(session_id, "")
    await websocket.send_text(current_content)
    
    try:
        while True:
            data = await websocket.receive_text()
            storage[session_id] = data
            await manager.broadcast(data, session_id, exclude=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
