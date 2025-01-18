import socket
import threading

def handle_send(sock):
    """发送线程，负责从用户输入中发送消息"""
    while True:
        message = input("You (App2): ")  # 从控制台读取输入
        sock.sendall(message.encode())
        if message.strip().upper() == "END":  # 如果发送 END，结束通信
            break

def handle_receive(sock):
    """接收线程，负责接收消息并显示"""
    while True:
        data = sock.recv(1024)
        if not data:
            break
        message = data.decode().strip()
        if message.upper() == "END":  # 对方发送 END，结束通信
            print("App2: Connection ended by the other side.")
            break
        print(f"App1: {message}")

if __name__ == "__main__":
    # 创建 Socket 通信
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))  # 连接到 App1 的服务端

    # 启动发送和接收线程
    send_thread = threading.Thread(target=handle_send, args=(client_socket,))
    receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_socket.close()
    print("App2 finished")
