from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import socket
import threading
import json

ADMIN_ADDR = socket.gethostbyname(socket.gethostname())
#Port
ADMIN_PORT = 5505 

print(ADMIN_ADDR)

FORMAT = "utf8"
MAX_CILENT = 10

COLOR_1 = "#040073"
COLOR_2 = "#1337ac"
COLOR_3 = "#617dd7"
COLOR_4 = "#ffffff"


user_list = {} # list of user
class Admin:
    def __init__(self):
        """
        It creates a GUI for the admin to see the list of online users and the list of offline users.
        """
        #Back End
        
        # Creating a socket object and binding it to the host and port.
        self.host_server = socket.gethostbyname(ADMIN_ADDR)
        self.port_server = ADMIN_PORT
        self.curr_client = 0

        # Creating a socket object.
        self.server_process = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Binding the server to the host and port.
        self.server_process.bind((self.host_server, self.port_server))
        # The above code is listening for 10 connections.
        self.server_process.listen(10)
        
        #Front End
        
        # Creating a GUI window with a title, size, and color.
        self.gui = Tk()
        self.gui.title("ADMIN GUI")
        self.gui.geometry("600x600")
        self.gui.protocol("WM_DELETE_WINDOW", self.Close)
        #ID Frame
        self.Frame = Frame(self.gui)
        self.Id_Room = Label(self.Frame, text="ID ROOM")
        self.idLabel = Label(self.Frame, text="WELCOME TO ADMIN GUI")
        self.Input = Label(self.Frame, text=self.host_server)
        self.idLabel.config(font=("Arial", 25), bg=COLOR_1, fg=COLOR_4)
        self.idLabel.pack()
        
        
        
       # The above code is creating a GUI for the chat application.
        self.Frame.config(bg=COLOR_2)       
        self.Id_Room.config(bg=COLOR_1, fg=COLOR_4)
        self.Input.config(bg="#ffffff", fg=COLOR_1)
        self.Frame.place(relheight=0.34, relwidth=1)
        self.Id_Room.place(relheight=0.15, relwidth=0.3, relx=0.35, rely=0.32)
        self.Input.place(relheight=0.15, relwidth=0.3, relx=0.35, rely=0.52)
        self.Act_Frame = Frame(self.gui)
        self.Online_Frame = Frame(self.Act_Frame)       
        self.onlIntro = Label(self.Online_Frame, text="LIST OF ONLINE USER")
        self.Online_Frame.config(bg = COLOR_4)
        self.Act_Frame.config(bg = COLOR_2)
        self.onlIntro.config(bg = COLOR_1, fg = COLOR_4)
        self.Online_Frame.place(relheight=0.55, relwidth=0.7, relx=0.15, rely=0.11)
        self.Act_Frame.place(relheight=0.9, relwidth=1, relx=0,rely=0.3)
        self.onlIntro.place(relheight=0.1, relwidth=0.6, relx=0.2,rely=0.02)
        
        
        self.Online_User = []
        #self.offUser = []


#------------------------ BASIC FUNCTION ---------------------   
    #server-process listen to client
    def listen(self):                           
        """
        The function listens for new clients and creates a new thread for each client
        """
        while self.curr_client<MAX_CILENT: # no more than 10 clients
            # accept new client and create a new thread for it
            channel,client = self.server_process.accept() 
            print(f"Client: {client}") # print client address
            try: # try to create a new thread
                self.curr_client += 1 # get new client
                thr = threading.Thread(target=self.userHandle, args=(channel,client)) # create new thread
                thr.daemon = False # set daemon to False
                thr.start() # start thread
            except: 
                print("error") # print error
    #server-process recieve message from other
    def receive_message(self, channel, client):        
        """
        It receives a message from the client and returns it
        
        :param channel: the channel that the message is being received from
        :param client: the client object
        :return: The message that was received.
        """
        mess = channel.recv(1024).decode(FORMAT) # receive message
        return mess
    #server-process Send_mess message to other
    def Send_mess(self, channel, client, message): # Send_mess message to client    
        """
        It sends a message to a client
        
        :param channel: the socket
        :param client: the client that the message is being sent to
        :param message: the message to Send_mess
        """
        channel.sendall(str(message).encode(FORMAT)) # Send_mess message
        
        
    #fucntion support for close the connection
    def Close(self): 
        self.server_process.close() # close server
        self.gui.destroy() # close gui
    #function support for update user list
    
    
    
    
    
    #function support for Authentification    
    def processAccount(self, acc, adr):
        """
        It takes a string of the form "name:password" and "address:port" and returns a dictionary with
        the keys "name", "password", "address", "port", and "isAct" with the values being the
        corresponding values from the input strings
        
        :param acc: {'name': 'password'}
        :param adr: {'127.0.0.1': '8080'}
        :return: A dictionary with the keys "name", "password", "address", "port", and "isAct".
        """
        Information = {}
        # Replacing the curly braces, single quotes, and spaces with nothing.
        accInfor=acc.replace("{","").replace("}","").replace("'","").replace(" ","").split(":")
        adrInfor=adr.replace("{","").replace("}","").replace("'","").replace(" ","").split(":")
        # Creating a dictionary called Information and adding the values of the accInfor and adrInfor
        # lists to it.
        Information["name"] = accInfor[0]
        Information["password"] = accInfor[1]
        Information["address"] = adrInfor[0]
        Information["port"] = adrInfor[1]
        Information["isAct"] = 1
        
        return Information
    
    
    def checkAccount(self, jsonFile, jsonObject):
        """
        If the name and password in the jsonObject match the name and password in the jsonFile, then
        update the address, port, and isAct fields in the jsonFile
        
        :param jsonFile: the json file that contains all the accounts
        :param jsonObject: {"name": "name", "password": "password", "address": "address", "port":
        "port"}
        :return: The jsonFile and the message
        """
        for account in jsonFile["account"]:
            if account["name"] == jsonObject["name"] and account["password"]==jsonObject["password"]: 
                account["address"] = jsonObject["address"]
                account["port"] = jsonObject["port"]
                account["isAct"] = 1
                return jsonFile, "SUCCESS"
        return jsonFile, "FAILED"
    
    
    def createAccount(self, jsonFile, jsonObject):
        """
        It takes a json file, and a json object, and appends the json object to the json file
        
        :param jsonFile: The json file that is being read from
        :param jsonObject: {"name": "John", "age": 30, "city": "New York"}
        :return: The jsonFile and the "SUCCESS"
        """
        jsonFile["account"].append(jsonObject)
        return jsonFile, "SUCCESS"
    
    
    def Deactive_acc(self, userName):
        """
        It opens the json file, finds the account with the name that matches the userName parameter,
        sets the isAct value to 0, and then dumps the json file
        
        :param userName: The name of the user to be deactivated
        """
        with open("account.json", "rb") as f:
            jsonFile = json.load(f)
        
        for account in jsonFile["account"]:
            if account["name"] == userName:
                account["isAct"] = 0
        with open('account.json','w') as f:
            json.dump(jsonFile,f)   

        self.updateUserList()
#------------------------ SERVER PROCESS ---------------------
    #FOR ADMIN USER
    # Enforce normal user to  login before allow them to chat with other
    def userHandle(self,channel, client):
        """
        The function userHandle() is called when a user connects to the server. It calls the
        userAuthen() function to authenticate the user, then calls the updateUserList() function to
        update the user list, and finally calls the userChat() function to allow the user to chat
        
        :param channel: The channel that the user is in
        :param client: The client object that is connected to the server
        """
        self.user_Authentication(channel, client)
        self.updateUserList()
        self.userChat(channel, client)
        
    # Authentification for normal user
    
    
    def user_Authentication(self, channel, client):
        """
        It receives a message from the client, then sends a message back to the client to ensure that
        the client receives the message in order
        
        :param channel: the channel that the client is connected to
        :param client: the client socket
        """
        acc = None
        mess = None
        while mess!="SUCCESS":
            print("-------------------------------------------")
            mode = self.receive_message(channel,client)
            self.Send_mess(channel, client, "Received")      # ensure client receive inorder
            acc = self.receive_message(channel, client)
            self.Send_mess(channel, client, "Received")      # ensure client receive inorder
            adr = self.receive_message(channel , client)
            self.Send_mess(channel, client, "Received") 
            
            # Update 
            jsonObject = self.processAccount(acc, adr)
            print(jsonObject)
            with open("account.json", "rb") as f:
                jsonFile = json.load(f)

            print(self.receive_message(channel , client))
            if int(mode)==1:  #login
                jsonFile, mess = self.checkAccount(jsonFile, jsonObject)
                self.Send_mess(channel, client, mess)
            elif int(mode)==2: #signing2
                jsonFile, mess = self.createAccount(jsonFile, jsonObject)
                self.Send_mess(channel, client, mess)
            print(self.receive_message(channel, client))

            with open('account.json','w') as f:
                json.dump(jsonFile,f)

            print("-------------------------------------------")
            
    def updateUserList(self):
        """
        It reads a json file, creates a dictionary, loops through the json file, creates a label for
        each account, places the label in a frame, and then writes the json file.
        """
        with open("account.json", "rb") as f: 
            jsonFile = json.load(f) # read json file
        self.Online_User = {} # create new dictionary
        
        for account in jsonFile["account"]: # loop through all account
            # Creating a new label with the name of the account.
            self.Online_User[account["name"]] = Label(self.Online_Frame, text=account['name']) 
            self.Online_User[account["name"]].config(bg=COLOR_1, fg=COLOR_4) 

        # A variable to keep track of the index of the label.
        onlIndex = 0
        
        for widget in self.Online_Frame.winfo_children():
            widget.place(relheight=0, relwidth=0)

        self.onlIntro.place(relheight=0.1, relwidth=0.3, relx=0.2)
        # This is a loop that goes through all the accounts in the json file and checks if the account
        # is active. If it is, it will add 1 to the index and place the label in the frame.
        for account in jsonFile["account"]:
            if account["isAct"] == 1:
                onlIndex+=1
                self.Online_User[account["name"]].place(relheight=0.1, relwidth = 0.8, relx=0.1, rely =  onlIndex*0.15)

        with open('account.json','w') as f:
            json.dump(jsonFile,f) 
        pass
            
            
    # Communication with Normal User
    def userChat(self, channel, client):
        """
        The function receives a message from the client, then sends a message to the client, then
        deactivates the account, then decrements the current client count
        
        :param channel: the channel that the client is connected to
        :param client: The client that is currently connected to the server
        """

        friendID = 0
        # Sending the json file to the client.
        while friendID != -1:
            print("check")
            if friendID>=-1 or friendID==-2:
                with open("account.json", "rb") as f:
                    jsonFile = json.load(f)                   # load json filefA
                    self.Send_mess(channel, client, json.dumps(jsonFile))    # Send_mess json file
                    self.receive_message(channel, client)           # receive message
            
            # Receiving a friendID from the client and sending a message back to the client.
            friendID = int(self.receive_message(channel, client)) # receive friendID
            self.Send_mess(channel, client, "Received") # Send_mess


       # Receiving a message from the client, then sending a message to the client, then deactivating
       # the account, then decrementing the current client count.
        userName = self.receive_message(channel, client) 
        self.Send_mess(channel, client, "Diconnected")
        self.Deactive_acc(userName)
        self.curr_client -= 1
    
    # Admin user just have server-process, which keeps track on database, normal user Informationmation

# The above code is creating a new thread and starting it.
if __name__=="__main__":
    print("Messenger Clone: Admin")
    admin = Admin()
    
    
    # Creating a thread that will run the admin.listen() function.
    thread = threading.Thread(target = admin.listen)
    # Setting the thread to be a daemon thread.
    thread.daemon= True
    # The above code is creating a new thread and starting it.
    thread.start()

    # Creating a GUI window with a title of "Admin" and a label of "Python".
    admin.gui.mainloop()
   