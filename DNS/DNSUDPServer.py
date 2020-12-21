"""DNSUDPServer.py

This script sets up a DNS server - it recieves requests in port 53,
decodes them, asks the blockchain for answers, and sends replies.

TODO: Add API to blockchain, test if handles all types of requests and questions f.e A, AAAA reversed, other dns logics etc.
TODO: Handle exceptions such as no connection to blockchain, address not found(send no-existent domain)
"""

import socket
import dnslib

# DNS server interface IP.
IP = "127.0.0.1"

# DNS server port.
PORT = 53

# Packet buffer size. buffer size 512 as mentioned in DNS RFC.
BUFFER_SIZE = 512

def lookup_name(name):
    """
    Recives a name, looks it up in the blockchain,
    returns corresponding address if found.
    """
    
    return("1.2.3.4")

def main():

    # Creates internet UDP socket.
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # Binds to the specified IP and port.
    sock.bind((IP, PORT))

    while True:

        # Recives data (DNS request) and address from a client. buffer size 512 as mentioned in DNS RFC.
        data, addr = sock.recvfrom(BUFFER_SIZE)

        # Informs in the console about a request recived.
        print ('Recieved request from {0} at port {1}.'.format(addr[0], addr[1]))

        try:
            
            # Decodes data to DNS request.
            dns_req = dnslib.DNSRecord.parse(data)
        
        except:
        
            # Informs in the console that the request is corrupted.
            print("Failed decoding the request due to corruption.")
        
        else:
            
            # For each question in the clients DNS request:
            for question in dns_req.questions:

                # Gets the name queried in the question.
                q_name = question.get_qname()

                # Generates a reply to the client.
                dns_rep = dnslib.DNSRecord(dnslib.DNSHeader(id=dns_req.header.id,qr=1,aa=1,ra=1),q=dnslib.DNSQuestion(q_name),a=dnslib.RR(q_name,rdata=dnslib.A(lookup_name(q_name))))
                
                try:
                
                    # Sends the reply generated to the client.
                    sock.sendto(bytes(dns_rep.pack()), addr)
                
                except:
                
                    # Informs in the console that sending the reply failed.
                    print("Failed sending reply.")
                
                else:
                
                    # Informs in the console about a reply sent.
                    print ('Sent reply to {0} at port {1}.\n'.format(addr[0], addr[1]))

if __name__ == "__main__":
    main()
