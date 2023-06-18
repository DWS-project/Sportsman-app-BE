import socketio

sio = socketio.Client()


def send_socket_message(event, data):
    sio.connect('http://localhost:3000')
    sio.emit(event, data)
    sio.wait()
