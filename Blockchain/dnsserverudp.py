import socket
import dnslib
import binascii

# DNS server interface IP.
IP = "127.0.0.1"

# DNS server port.
PORT = 53

# Packet buffer size.
BUFFER_SIZE = 512

# Creating internet UDP socket.
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Binding to the specified IP and port.
sock.bind((IP, PORT))

while True:

    # Reciving data and address from a client. buffer size 512 as in DNS RFC.
    data, addr = sock.recvfrom(BUFFER_SIZE)
    d = dnslib.DNSRecord(dnslib.DNSHeader(qr=1,aa=1,ra=1),q=dnslib.DNSQuestion("abc.com"),a=dnslib.RR("abc.com",rdata=dnslib.A("1.2.3.4")))

    # Informing in the console about a request recived.
    print ('\nRecieved request from {0} at port {1}'.format(addr[0], addr[1]))

    # Decoding data to dns request.
    packet = binascii.unhexlify(data.hex())
    d = dnslib.DNSRecord.parse(packet)

    # Examples of the data we can extract from a dns request or reply. I tried making it look like wireshark.
    print ("HEADER_QR:{0}".format(d.header.get_qr()))
    print ("HEADER_OPCODE:{0}".format(d.header.get_opcode()))
    print ("HEADER_AA:{0}".format(d.header.get_aa()))
    print ("HEADER_TC:{0}".format(d.header.get_tc()))
    print ("HEADER_RD:{0}".format(d.header.get_rd()))
    print ("HEADER_RA:{0}".format(d.header.get_ra()))
    print ("HEADER_Z:{0}".format(d.header.get_z()))
    print ("HEADER_AD:{0}".format(d.header.get_ad()))
    print ("HEADER_CD:{0}".format(d.header.get_cd()))
    print ("HEADER_RCODE:{0}".format(d.header.get_rcode()))
    print ("NUM_OF_QUESTIONS:{0}".format(len(d.questions)))
    print ("NUM_OF_ANSWER_RRs:{0}".format(len(d.rr)))
    print ("NUM_OF_AUTH_RRs:{0}".format(len(d.auth)))
    print ("NUM_OF_ADDITIONAL_RRs:{0}".format(len(d.ar)))
    print ("QUESTIONS_SECTION:")
    for question in d.questions:
        print ("    NAME:{0}\n    TYPE:{1}\n    CLASS:{2}\n".format(question.get_qname(), dnslib.CLASS.get(question.qclass), dnslib.QTYPE.get(question.qtype)))
    print ("ANSWERS_SECTION:")
    for answer in d.rr:
        print ("    NAME:{0}\n    TYPE:{1}\n    CLASS:{2}\n   TTL:{2}\n   RDATA:{2}\n".format(answer.get_rname(), dnslib.QTYPE.get(answer.rtype), dnslib.CLASS.get(answer.rclass), answer.ttl, answer.rdata.toZone()))

    #print(d) # works to, but the above example shows how to access each individual values we need.

