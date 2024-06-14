import socket
import threading
import json
from GameState import GameState

HOST = 'localhost'
PORT = 12345


class Server:
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()
        self.min_players = 2
        self.max_players = 4
        self.active_connections = 0
        self.game_state = {
            'round_number': 1,
            'players': [],
            'game_status': GameState.HOMESCREEN.value,
            'dice_values': [0, 0],
            'fighting_players': []
        }

    def send_game_state_to_all_clients(self, game_state):
        serialized_state = json.dumps(game_state)
        for client_socket in self.clients:
            client_socket.send(serialized_state.encode('utf-8'))

    def handle_client(self, client_socket, client_address):
        print(f"New connection from {client_address}")

        # Assign a player number
        with self.lock:
            player_number = len(self.game_state['players']) + 1
            player_data = {
                'number': player_number,
                'position': (0, 0),
                'type': 'UNDEFINED',
                'health': 30,
                'attack': 10,
                'maxrange': 5,
                'inventory': [],
                'canFight': True,
                'isWinner': False
            }
            self.game_state['players'].append(player_data)
            self.active_connections += 1
            self.clients.append(client_socket)

            # Send initial game state to new client
            client_socket.send(json.dumps(self.game_state).encode('utf-8'))

            # Wait until the minimum number of players is reached
            if len(self.clients) >= self.min_players:
                self.game_state['game_status'] = GameState.CHOOSEMENU.value
                self.broadcast_game_state()

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    action = json.loads(message)
                    with self.lock:
                        self.process_action(action)
                        self.broadcast_game_state()
            except ConnectionResetError:
                print(f"Disconnected from {client_address}")
                with self.lock:
                    self.clients.remove(client_socket)
                    self.active_connections -= 1
                client_socket.close()
                break

    def process_action(self, action):
        if action['type'] == 'move':
            player = next(p for p in self.game_state['players'] if p['number'] == action['player'])
            player['position'] = action['position']
            self.game_state['round_number'] = (self.game_state['round_number'] % len(self.game_state['players'])) + 1
    
    def update_game_state(self, action, player_number):
        # Update the game state based on the action and player number
        if action['type'] == 'MOVE_PLAYER':
            self.game_state['players'][player_number - 1]['position'] = action['new_position']
        elif action['type'] == 'ROLL_DICE':
            self.game_state['dice_values'] = action['dice_values']

        # Send the updated game state to all clients
        self.send_game_state_to_all_clients(self.game_state)

    def broadcast_game_state(self):
        message = json.dumps(self.game_state)
        for client in self.clients:
            client.send(message.encode('utf-8'))

   def start_server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started and listening on port", PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            with self.lock:
                if len(self.clients) < self.max_players:
                    threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
                else:
                    client_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start_server()
