import socket               # allows network communication
import threading            # allows simultaneous message tx and rx
import base64               # to encode/decode binary
from crypto_utils import generate_aes_key, encrypt_with_rsa

clients = {}                        # tracks clients
aes_key = generate_aes_key()        # using shared AES key

# loop to handle incoming client messages
def handle_messages(sock):                      # takes parameter "sock"
    while True:
        data, addr = sock.recvfrom(4096)        # wait to receive data from any client
                                                # accepts 4096 byte messages
        if addr not in clients:
            # First message = RSA public key
            try:
                # decode RSA public key from client
                rsa_pub_key = base64.b64decode(data)

                # encrypt AES key with client's RSA key
                encrypted_key = encrypt_with_rsa(rsa_pub_key, aes_key)

                # send AES key back to client
                sock.sendto(base64.b64encode(encrypted_key), addr)

                # if connected then true
                clients[addr] = True
                #debug message
                print(f"Key exchanged with {addr}")

            # catches exception if key exchange failed    
            except Exception as e:
                print(f"Key exchange failed for {addr}: {e}")

        # client completed key exchange        
        else:
            # Broadcast to all other clients
            for client_addr in clients:
                if client_addr != addr:
                    sock.sendto(data, client_addr)


def main():

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # connect socket to interface on port 12345
    sock.bind(("localhost", 12345))

    # server is listening
    print("Server started on port 12345")

    # handle messages in loop
    handle_messages(sock)

# start server
if __name__ == "__main__":
    main()
