import sys
import tkinter

from src import game

USAGE = "\nUsage: python main.py <server_host> <server_port> <client_port>"
def main():

    # Create GUI
    root = tkinter.Tk()
    root.title("A Game")
    root.geometry("500x500")
    
    # Textbox for server host
    host_label = tkinter.Label(root, text="Host IP:")
    host_label.pack()
    host_textbox = tkinter.Entry(root, bd = 5)
    host_textbox.pack()

    # Textbox for client port
    port_label = tkinter.Label(root, text="Port:")
    port_label.pack()
    port_textbox = tkinter.Entry(root, bd = 5)
    port_textbox.pack()

    def connect():
        host = host_textbox.get()
        port = port_textbox.get()
        print(host, port)

    # Connect button
    button = tkinter.Button(root, text="Connect", command = connect)

    button.pack()
    root.mainloop()

    '''
    filename, server_host, server_port, client_port = sys.argv
    try:
        game.Game(server_host, int(server_port), int(client_port))
    except ValueError:
        print("[Error]: Port must be an integer")
        print(USAGE)

    return 0
    '''


if __name__ == "__main__":
    main()
