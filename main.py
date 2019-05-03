import sys
import tkinter

from src.game import Game
from src.network import Network

#TODO: Change errors from printing to console to printing on GUI
def main():

    # Get server info using tkinter GUI
    network = get_connection()

    if network:
        # Start game
        Game(network)

    return 0

def get_connection():
    """
    Create a GUI window using tkinter
    to get IP and port from user.

    Loops until successful connection is made.
    
    Returns:
        {Network} -- Used to send/receive data from server
    """

    # Hold network object in list
    # If list is empty, no connection
    connection = []

    # Greate GUI
    root = tkinter.Tk()
    root.title("A Game of Shapes")
    root.geometry("500x500")

    # Textbox to get server host
    host_label = tkinter.Label(root, text="Host IP:")
    host_label.pack()
    host_textbox = tkinter.Entry(root, bd=5)
    host_textbox.pack()

    # Textbox for server port
    port_label = tkinter.Label(root, text="Port:")
    port_label.pack()
    port_textbox = tkinter.Entry(root, bd=5)
    port_textbox.pack()

    #Console out
    # TODO: Fix console out by deleting previous content also make unwritable?
    T = tkinter.Text(root, height=2, width=50)
    T.pack(side = tkinter.BOTTOM)
    port_label = tkinter.Label(root, text="Console:")
    port_label.pack(side = tkinter.BOTTOM)
    T.insert(tkinter.END, "Errors are displayed here.")
    

    def add_network():
        """
        Grabs IP and port from textboxes and
        attempt to create a network connection.
        """

        host = host_textbox.get()
        port = port_textbox.get()

        # Create network object
        network = None
        try:
            network = Network(host, int(port))
        except:
            print("[Error]: Invalid ip address or port number")
            T.insert(tkinter.END, "[Error]: Invalid ip address or port number")

        connection.append(network)

        attempt_connection()
    
    def attempt_connection():
        """
        Connect using given address.
        If successful, closes window
        and returns network object.

        Returns:
            {Network} -- Represents connection to server
        """
        network = connection.pop()

        if network is not None:
            try:
                network.connect()
                connection.append(network)
                root.destroy()
            except:
                print("[Error]: Unable to connect to given address")
                T.insert(tkinter.END, "[Error]: Unable to connect to given address")
        
    def enter(event):
        '''
        Handle enter key press.
        Runs add_network().

        '''
        add_network()

    # Bind enter key to function
    root.bind("<Return>", enter)

    button = tkinter.Button(root, text="Connect", command=add_network)
    button.pack()
    
    

    root.mainloop()

    if connection:
        network = connection.pop()
        return network
    return None

if __name__ == "__main__":
    main()
