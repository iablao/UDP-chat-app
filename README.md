Overview:
This program is a UDP based chat application. We are using two different encryption methods - RSA and AES. The keys are implemented in crypto_utils.py using the pycryptodome library. A summary for each program file can be found below:

cypto_utils.py
    - Cryptographic operations
    - Generates RSA and AES keys
        - RSA encrypts/decrypts AES key
        - AES encrypts/decrypts messages

server.py
    - Listens for a client's RSA public key
    - Sends back AES key for that client, encrypted using RSA
    - Broadcasts ecrypted messages from a client to other clients

client.py
    - Generates RSA key pair
    - Sends the public key to the server
    - Decrypts received AES key using the private RSA key
    - Uses AES to encrypt/decrypt messages for communication

To launch the application:
1. Run python server.py in the terminal
2. Wait for debug message indicating "Server started on port 12345"
3. Run python client.py in the terminal
4. Choose username for identification.
5. Wait for debug message "Received and decrypted AES key."
6. Add another client (from another terminal) to the server using the same steps as 3-5
7. Send messages from either client and observe how the other client is receiving the messages
