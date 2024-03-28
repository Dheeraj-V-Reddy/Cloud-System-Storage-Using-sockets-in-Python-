from tkinter import filedialog, messagebox
import os
import socket
import time
import tkinter as tk
import ctypes
from tkinter import PhotoImage
import ssl
#import PIL.Image as Image
#import PIL.ImageTk as ImageTk

server_name = "192.168.56.1"
server_port = 17000
buffer = 4096

CERTFILE='C:\C_programs\cn project\server_cert.pem'     

class CloudClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SSLclientSocket = ssl.wrap_socket(self.client_socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=CERTFILE)

        self.SSLclientSocket.connect((server_name, server_port))
        self.user=""
        self.root = tk.Tk()
        self.root.title("Cloud Storage")
        self.bg_image = tk.PhotoImage(file=r"C:/C_programs/cn project/omg.png")

        self.fp()

    def create_widgets(self):
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.heading_label = tk.Label(text="C L O U D", font=("Verdana", 40, "bold"), bg="#a3b18a", fg="white")
        self.heading_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.upload_button = tk.Button(text="Upload File", command=self.upload_file, bg="#fefae0", fg="#283618", padx=20, pady=10, font=("Arial", 12, "bold"))
        self.upload_button.place(relx=0.3, rely=0.4, anchor=tk.CENTER)

        self.download_button = tk.Button(text="Download File", command=self.download_file, bg="#fefae0", fg="#283618", padx=20, pady=10, font=("Arial", 12, "bold"))
        self.download_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.delete_button = tk.Button(text="Delete File", command=self.delete_file, bg="#fefae0", fg="#283618", padx=20, pady=10, font=("Arial", 12, "bold"))
        self.delete_button.place(relx=0.7, rely=0.4, anchor=tk.CENTER)

        self.file_listbox = tk.Listbox(width=50, height=10, font=("Verdana", 10, "bold"), bg="#EDF8FA")
        self.file_listbox.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.refresh_button = tk.Button(text="Refresh List", command=self.refresh_list, bg="#fefae0", fg="#283618", padx=10, pady=5, font=("Arial", 10, "bold"))
        self.refresh_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            self.SSLclientSocket.sendall(self.user.encode())
            self.SSLclientSocket.sendall(b'1')  
            self.SSLclientSocket.sendall(file_name.encode())

            with open(file_path, "rb") as f:
                while True:
                    file_content = f.read(buffer)
                    if not file_content:
                        break
                    self.SSLclientSocket.sendall(file_content)

            print("File uploaded successfully.")
            messagebox.showinfo("Upload Success", "File uploaded successfully.")
            time.sleep(1)
            self.root.destroy()
        else:
            print("File upload failed")
            messagebox.showerror("Upload Failed", "No file selected for upload.")
        
        

    def download_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            save_path = filedialog.askdirectory()
            if save_path:
                self.SSLclientSocket.sendall(self.user.encode())
                self.SSLclientSocket.sendall(b'2')  
                self.SSLclientSocket.sendall(selected_file.encode())

                file_path = os.path.join(save_path, selected_file)
                with open(file_path, "wb") as f:
                    while True:
                        file_content = self.SSLclientSocket.recv(buffer)
                        if not file_content:
                            break
                        f.write(file_content)

                print("File downloaded successfully.")
                messagebox.showinfo("Download Success", "File downloaded successfully.")
            time.sleep(1)
            self.root.destroy()
        else:
            print("File was not selected")
            messagebox.showerror("Download Failed", "No file selected for download.")

    def remove_components(self):
        for widget in self.root.winfo_children():
            if widget != self.root:
                widget.destroy()
    def delete_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            self.SSLclientSocket.sendall(self.user.encode())
            self.SSLclientSocket.sendall(b'3') 
            self.SSLclientSocket.sendall(selected_file.encode())

            response = self.SSLclientSocket.recv(buffer).decode()
            print(response)
            if response.startswith("File deleted"):
                messagebox.showinfo("Deletion Success", response)
            else:
                messagebox.showerror("Deletion Failed", response)
            time.sleep(1)
            self.root.destroy()
        else:
            print("File was not selected")
            messagebox.showerror("Deletion Failed", "No file selected for deletion.")


    def refresh_list(self):
        self.file_listbox.delete(0, tk.END)
        self.SSLclientSocket.sendall(self.user.encode())
        self.SSLclientSocket.sendall(b'4')
        files = self.SSLclientSocket.recv(buffer).decode().split("\n")
        for file in files:
            if file:
                self.file_listbox.insert(tk.END, file)

    def run(self):
        self.root.mainloop()

    def __del__(self):
        self.SSLclientSocket.close()
    
    def fp(self):
        def submit_input():
            input_text = entry.get()
            self.user=input_text
            print("Input received:", input_text)
            self.remove_components()
            self.create_widgets()
        self.root.title("Home Page")
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        print(screen_width, screen_height)

    # Set window size to screen resolution
        self.root.geometry(f"{1000}x{2000}")

    # Load background image and resize it to fit the screen
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        '''user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        self.root.geometry(f"{screen_width}x{screen_height}")

        image = Image.open("C:/college/IV SEM/CN/Project/2.png")
        image = image.resize((screen_width, screen_height))
        self.root.background_image = ImageTk.PhotoImage(image)

        self.root.background_label = tk.Label(self.root, image=self.root.background_image)
        self.root.background_label.place(x=0, y=0, relwidth=1, relheight=1)'''
        self.root.title("Input Box GUI")
        label = tk.Label(self.root, text="Enter your Name",font=("Verdana", 20, "bold"), bg="#a3b18a", fg="white")
        label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        entry = tk.Entry(self.root)
        entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        submit_button = tk.Button(text="Enter", command=submit_input, bg="#fefae0", fg="#283618", padx=20, pady=10, font=("Arial", 12, "bold"))
        submit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
if __name__ == "__main__":
    client = CloudClient()
    client.run()
