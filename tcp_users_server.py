import socket


class TCPServer:

    def __init__(self, host, port, count_connetions):
        self.host = host
        self.port = port
        self.count_connetions = count_connetions
        self.server_socket = None
        self._history = []

    def server_init(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.count_connetions)
        print("Сервер запущен и ждет подключений...")

    def get_history(self):
        return "\n".join(self._history)

    def start_listening(self):
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Пользователь с адресом: {address} подключился к серверу")

                message = client_socket.recv(1024).decode()
                print(
                    f"Пользователь с адресом: {address} отправил сообщение: {message}"
                )

                self._history.append(message)

                client_socket.send(self.get_history().encode())
                client_socket.close()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("Остановка сервера...")
        self.server_socket.close()


if __name__ == "__main__":
    server_tcp = TCPServer(
        host="localhost",
        port=12345,
        count_connetions=10,
    )
    server_tcp.server_init()
    server_tcp.start_listening()
