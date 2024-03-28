from socket import *
import os
import threading
import ssl

CERTFILE = "server_cert.pem"
KEYFILE = 'server_key.pem'
server_port = 17000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(5)

shared_path = r"D:\server"

print("Server is active")




def handle_client(channel_socket):
    def refresh_file_list(channel_socket):
        files = os.listdir(folder_path)
        file_list = "\n".join(files)
        channel_socket.sendall(file_list.encode())
    user=channel_socket.recv(1024).decode()
    print(user)
    choice = channel_socket.recv(1).decode()
    c = int(choice)
    folder_path = os.path.join(shared_path,user)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{user}' created successfully in '{shared_path}'.")
        file_path = os.path.join(folder_path,"welcome.txt")
        with open(file_path,"wb") as f:
            f.write("Welcome to your cloud"+user)
    else:
        print(f"Folder '{user}' already exists in '{shared_path}'.")

    if c == 1: 
        file_name = channel_socket.recv(1024).decode()
        print("Uploading:", file_name)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as f:
            while True:
                file_content = channel_socket.recv(4096)
                if not file_content:
                    break
                f.write(file_content)
        print("File uploaded")
        

    elif c == 2:
        file_name = channel_socket.recv(107).decode()
        print("Downloading:", file_name)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "rb") as f:
            while True:
                file_content = f.read(4096)
                if not file_content:
                    break
                channel_socket.sendall(file_content)
        print("File sent")

    elif c == 3:
        file_name = channel_socket.recv(4096).decode()
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            channel_socket.send("File deleted successfully.".encode())
        else:
            channel_socket.send("ERROR: File not found.".encode())

    elif c == 4:
        print("Refreshing file list")
        refresh_file_list(channel_socket)
        handle_client(channel_socket)

    channel_socket.close()


while True:
    channel_socket, addr = server_socket.accept()
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    ssl_channelSocket = ssl_context.wrap_socket(channel_socket, server_side=True)

    thread = threading.Thread(target=handle_client,args=(ssl_channelSocket,))
    thread.start()
    print(f"Active connections   {threading.active_count() - 1}")
    