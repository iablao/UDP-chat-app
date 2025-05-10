import socket               # allows network communication
import threading            # allows simultaneous message tx and rx
import base64               # to encode/decode binary
from crypto_utils import (
    generate_rsa_keypair, decrypt_with_rsa,
    encrypt_with_aes, decrypt_with_aes
)

# holds AES key from server
aes_key = None

def receive_messages(sock, private_key):
    global aes_key
    while True:

        # wait for message from server
        data, _ = sock.recvfrom(4096)       # 4096 byte message

        # first message from server
        if aes_key is None:

            # decode from base64
            encrypted_key = base64.b64decode(data)

            # decrypt with RSA key
            aes_key = decrypt_with_rsa(private_key, encrypted_key)     
            print("Received and decrypted AES key.")
        else:

            # enable AES encrypted chat messaging
            try:
                # decrypt message and display
                decrypted = decrypt_with_aes(aes_key, data.decode())
                print(decrypted)

            # catch exception
            except Exception as e:
                print("Error decrypting message:", e)

# to identify clients
username = input("Enter your username: ")

def main():

    # assign decrypted AES key
    global aes_key

    # addr of server
    server_addr = ("localhost", 12345)

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate RSA keys and send public key
    private_key, public_key = generate_rsa_keypair()
    sock.sendto(base64.b64encode(public_key), server_addr)

    # Start thread to receive messages
    threading.Thread(target=receive_messages, args=(sock, private_key), daemon=True).start()

    # loop to hangle user input and output
    while True:

        # wait for user input 
        msg = input()
        if aes_key:

            # prefix with client that is talking
            full_msg = f"[{username}] {msg}"

            # encrypt with shared AES key
            encrypted = encrypt_with_aes(aes_key, full_msg) 
            
            # send to server
            sock.sendto(encrypted.encode(), server_addr)
        else:
            print("Waiting for key exchange to complete...")

if __name__ == "__main__":
    main()

