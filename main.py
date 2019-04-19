import sys
from src import game

USAGE = "\nUsage: python main.py <server_host> <server_port> <client_port>"
def main():
    filename, server_host, server_port, client_port = sys.argv
    try:
        game.Game(server_host, int(server_port), int(client_port))
    except ValueError:
        print("[Error]: Port must be an integer")
        print(USAGE)

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(USAGE)
        sys.exit(1)
    main()
