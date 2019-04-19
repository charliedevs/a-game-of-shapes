import sys
from src import game

def main():
    filename, server_host, server_port, client_port = sys.argv
    try:
        game.Game(server_host, int(server_port), int(client_port))
    except ValueError:
        print("[Error]: Port must be an integer")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <server_host> <server_port> <client_port>")
        sys.exit(1)
    main()
