# Error-Detection-in-the-Data-Link-Layer

### Execution

#### Server
> python3 server.py <server_portNo>

#### Client
> python3 client.py <server_portNo>

Providing port number while execution is optional but if given, it must be provided for both the programs
### Summary
- It is a simple client-server programming model where client acts as transmitter and server acts as reciever.
- The error detection function used is CRC
- Key being used for CRC check is 4 bit string "1011" which is fixed on both client and server side.
- Only Client sends the encrypted message while server receives it and decrypts it.
- Hill cipher is used for encrypting the message.
- The cipher matrix is pre-fixed for simplicity.
- Multiple clients can be connected to the server. Server can serve atmost 5 clients at a time. This maximum limit can be changed if required.
