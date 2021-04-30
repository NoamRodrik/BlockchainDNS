0. Run Ganash server.
1. Run the script in .\BlockchainDNS\Blockchain\scripts\DNSUDPServer.py
2. WIN+R -> ncpa.cpl -> set 193.106.55.102 as your only DNS server.
3. Click on the links in the folder. some are websites I have hardcoded in the DNSUDPServer.py script for the sake of this demonstration.

* Demonstrate how we can browse to registered servers while we cant to non-registered servers.

4. WIN+R -> ncpa.cpl -> add 8.8.8.8 as a secondary DNS server to our server.

* Demonstrate how we can also browse to non-registered servers because they are registered to 8.8.8.8.
* This demonstrate how our server co-exists with other DNS servers.