import socket


class ClientTCP:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socket = None

    def client_init(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

    def send_message(self, message: str):
        self._socket.send(message.encode())

    def get_answer(self, size=1024):
        answer = self._socket.recv(size).decode()
        print(answer, end="\n\n")

    def client_close(self):
        self._socket.close()
        print("Клиент отключился", end="\n\n")


if __name__ == "__main__":
    client = ClientTCP(
        host="localhost",
        port=12345,
    )
    messages = ["Привет сервер!", "Как дела?", "Отлично!"]
    for msg in messages:
        client.client_init()
        print(f"Клиент отправил сообщение: {msg}")
        client.send_message(msg)
        print("Клиент получил ответ:")
        client.get_answer()
        client.client_close()
