from twilio.rest import Client
from tkinter import messagebox
import socket
from location import display_map



def get_ip_address():

    """ returns : IP address of machine connected within a network """

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(type(ip_address))
    return ip_address

def send_sms(recipient_number, message_body):

    """Function that sends message
    reciepant_number (str) = number you want to send message 
    message_body (str) = content of message"""

    # Your Twilio Account SID and Auth Token
    account_sid = 'your twilio account SID'
    auth_token = 'your twilio account Auth Token'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send SMS message
    message = client.messages.create(
        body=message_body,
        from_='Your Twilio phone number',
        to=recipient_number
    )

    print("Message SID:", message.sid)  # Print the unique ID of the message

# I used IP to create local host using Flask. open app.py for more info.
ip_address = get_ip_address()
link = f"http://{ip_address}:5000"



def SOS_message(sign_list , original_list ):

    if bool(sign_list)==False:

        send_sms('recievers mobile number ', f'Emergancy signal recieved!!! click on the link to see location : {link}')

        print("SOS message is sent!!!")
        messagebox.showinfo("MESSAGE","SOS message is sent!!!")

        display_map('latitude','longitude')
        print(original_list)
        sign_list = original_list
        return sign_list
    else:
        return sign_list


def pop_list(pass_list,c_count , a_count):

    """ takes 3 arguments : pass_list{list} , c_count{int} , a_count{int} 
    c_count and a_count --> counters of two hand signs used for SOS signal.
    pass_list --> list containing two hand sign as strings"""

    list_elements = len(pass_list)

    if list_elements == 2 :
        if c_count >= 5:
            pass_list.pop()
    elif list_elements == 1:
        if a_count >= 5:
            pass_list.pop()
    else:
        pass


"""SOS_message([],[1,233,4])"""