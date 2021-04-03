"""
DNSUDPServer.py

This script sets up a DNS server - it receives requests in port 53,
decodes them, asks the blockchain for answers, and sends replies.

TODO: Add API to blockchain, test if handles all types of requests and questions f.e A, AAAA reversed, other DNS logic etc.
TODO: Handle exceptions such as no connection to blockchain.
"""

import socket
import dnslib

# DNS server interface IP.
IP = "10.10.248.102"

# DNS server port.
PORT = 53

# Packet buffer size. Buffer size 512 as mentioned in DNS RFC.
BUFFER_SIZE = 512

def lookup(record_name, record_type):
    """
    Receives a record name (name or IP), record type (A, AAAA, etc.),
    looks it up in the blockchain database, returns the corresponding address if found.
    """
    
    # Hardcoded answers for the sake of the POC!!!
    if record_type == 'A':
        if record_name == 'he.wikipedia.org':
            return(["91.198.174.192"])

        elif record_name == 'www.google.com':
            return(["172.217.169.4"])

        elif record_name == 'github.com':
            return(["140.82.121.4"])

        else:
            return([])
    else:
        return([])

def main():

    # Creates internet UDP socket.
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # Binds to the specified IP and port.
    sock.bind((IP, PORT))

    while True:

        try:

            # Receives data (DNS request) and address from a client. buffer size 512 as mentioned in DNS RFC.
            data, addr = sock.recvfrom(BUFFER_SIZE)
        except:
            continue

        # Informs in the console about a request received.
        print ('Received request from {0} at port {1}.'.format(addr[0], addr[1]))

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

                # If the query type is PTR (reverse query).
                if dnslib.QTYPE.get(question.qtype) == 'PTR':
                    pass

                # If the query type is A (IPv4).
                if dnslib.QTYPE.get(question.qtype) == 'A':

                    # Generates reply.
                    dns_rep = dnslib.DNSRecord(dnslib.DNSHeader(id=dns_req.header.id,qr=1,aa=1,ra=1),q=dnslib.DNSQuestion(q_name,dnslib.QTYPE.A))

                    # Looks up answers, operates on each one if there are any.
                    for answer in lookup(q_name, 'A'):

                        # Adds the answer to the reply.
                        dns_rep.add_answer(dnslib.RR(q_name,dnslib.QTYPE.A,rdata=dnslib.A(answer)))

                # If the query type is AAAA (IPv6).
                if dnslib.QTYPE.get(question.qtype) == 'AAAA':

                    # Generates reply.
                    dns_rep = dnslib.DNSRecord(dnslib.DNSHeader(id=dns_req.header.id,qr=1,aa=1,ra=1),q=dnslib.DNSQuestion(q_name,dnslib.QTYPE.AAAA))

                    # Looks up answers, operates on each one if there are any.
                    for answer in lookup(q_name, 'AAAA'):

                        # Adds the answer to the reply.
                        dns_rep.add_answer(dnslib.RR(q_name,dnslib.QTYPE.AAAA,rdata=dnslib.AAAA(answer)))

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
