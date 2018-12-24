// my_javascript.js

document.addEventListener('DOMContentLoaded', () => {

	// Connect to websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


    socket.on('connect', () => {
        socket.emit('on connect');
        document.getElementById('send').onclick = function() {
            message = document.getElementById('message').value;
            socket.emit('send message', {'message': message, 'room': room });
            document.getElementById('message').value = '';
        }
    }
});