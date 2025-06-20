import socket
import argparse
import textwrap

# Create UDP or TCP echo server
def echo_receiver(proto, host, port):
    if proto.lower() == "udp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))
        print(f"UDP Echo Server listening on {host}:{port}...\nStop the server with ^C")

        try:
            while True:
                data, addr = server_socket.recvfrom(1024)
                print(f"Received from {addr}: {data.decode()}")
                server_socket.sendto(data, addr)
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        finally:
            server_socket.close()

    elif proto.lower() == "tcp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"TCP Echo Server listening on {host}:{port}...\nStop the server with ^C")

        try:
            while True:
                conn, addr = server_socket.accept()
                print(f"Connection from {addr}")
                try:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(f"Received: {data.decode()}")
                        conn.sendall(data)
                except ConnectionResetError:
                    print(f"Connection reset by {addr}")
                finally:
                    conn.close()
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        finally:
            server_socket.close()

# Create UDP or TCP echo client
def echo_sender(proto, host, port):
    if proto.lower() == "udp":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            while True:
                message = input("Enter message to send: ").strip()
                if not message:
                    continue
                client_socket.sendto(message.encode(), (host, port))
                data, _ = client_socket.recvfrom(1024)
                print(f"Echoed from server: {data.decode()}")
        except KeyboardInterrupt:
            print("\nClient stopped by user.")
        finally:
            client_socket.close()

    elif proto.lower() == "tcp":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
            while True:
                message = input("Enter message to send: ").strip()
                if not message:
                    continue
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                if not data:
                    print("Server closed the connection.")
                    break
                print(f"Echoed from server: {data.decode()}")
        except KeyboardInterrupt:
            print("\nClient stopped by user.")
        finally:
            client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jeroen's Echo tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''
            With this tool you can test TCP/UDP connections by letting the receiver listen on a port,
            and the sender send a message to that port.

            Examples:
              python3 echotool.py -r -t tcp -b 0.0.0.0 -p 55555           # TCP receiver
              python3 echotool.py -r -t udp -b 0.0.0.0 -p 55555           # UDP receiver
              python3 echotool.py -s -t tcp -b 10.0.0.50 -p 55555         # TCP sender
              python3 echotool.py -s -t udp -b 10.0.0.50 -p 55555         # UDP sender
            '''
        )
    )

    parser.add_argument('-r', '--receiver', action='store_true', help='create a listener for receiving messages')
    parser.add_argument('-s', '--sender', action='store_true', help='create a sender for sending messages')
    parser.add_argument('-t', '--protocol', choices=['tcp', 'udp'], required=True, help='protocol, can be tcp or udp')
    parser.add_argument('-b', '--bind', required=True, help='IP address to bind to or connect to')
    parser.add_argument('-p', '--port', type=int, default=55555, help='port number (default: 55555)')

    args = parser.parse_args()

    host = args.bind
    port = args.port
    proto = args.protocol

    if args.receiver:
        echo_reveiver(proto, host, port)
    elif args.sender:
        echo_sender(proto, host, port)
    else:
        print("Error: You must specify either --receiver (-r) or --sender (-s).")
        exit(1)
