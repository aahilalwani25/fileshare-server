from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

connected_clients = []


@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    client={
        'id':request.sid,
        'name': None,
        #'clientSocketID': None
    }
    connected_clients.append(client)

@socketio.on('set-name')
def handle_connect(data):
    print(f"Client connected: {request.sid}")

    for client in connected_clients:
        if client['id']== request.sid:
            client['name'] = data['name']
            #client['clientSocketID']= data['clientSocketID']

@socketio.on('disconnect')
def handle_disconnect():
    disconnected_client = None
    for client in connected_clients:
        if client['id'] == request.sid:
            disconnected_client = client
            connected_clients.remove(client)
            break

    if disconnected_client:
        print(f"Client disconnected: {disconnected_client['name']}")
        emit('client-disconnected', {'name': disconnected_client['name']}, broadcast=True)

# Socket.IO event for file upload
# @socketio.on('file_upload')
# def handle_file_upload(data):
#     filename = data['filename']
#     file_data = data['file']
#     recipient = data['recipient']  # Assuming client identifier is provided

#     # Determine the room or client ID based on recipient (e.g., username)
#     recipient_sid = clients.get(recipient)

#     if recipient_sid:
#         # Send the file to the specific client
#         emit('file_received', {'filename': filename, 'file': file_data}, room)
#     else:
#         print(f"Client '{recipient}' not found or not connected.")

@socketio.on('show-online-clients')
def show_online_clients():
    emit('online-clients',{'clients':connected_clients})

# @socketio.on('send-socket-info')
# def receive_socket_info(data):
#     client_socket= data['socket']
#     print('Received socket: ',client_socket)


@socketio.on('send-file')
def receive_file(data):
    filename = data['filename']
    file_data = data['file_data'] #base64
    recipient_sid = data['recipient']

    # Check if the recipient is connected
    recipient = next((client for client in connected_clients if client['id'] == recipient_sid), None)
    if recipient:
        # Send the file to the specific client
        print(recipient)
        #with open(filename, 'rb') as f:
            #file_content = f.read()
        emit('file-received', {'filename': filename, 'file': file_data}, room=recipient_sid)
        print(f"File {filename} sent to client {recipient_sid}")
    else:
        print(f"Client '{recipient_sid}' not found or not connected.")
    
    

@app.route('/')
def hello_world():
    return 'Hello from Flask!'



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
