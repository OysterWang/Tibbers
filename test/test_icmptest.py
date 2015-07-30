import socket
import struct

def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff 
        count = count + 2
    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff 
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def ping(ip):
    s=socket.socket(socket.AF_INET,socket.SOCK_RAW,255)
    s.setsockopt(0, socket.IP_HDRINCL, 1)
# now start constructing the packet
 
    source_ip = '192.168.4.135'
    dest_ip = ip
 
# ip header fields
    ihl = 5
    version = 4
    tos = 0
    tot_len = 28
    id = 0
    frag_off = 0
    ttl = 255
    protocol = 1
    check = 0  
    saddr =socket.inet_aton ( source_ip )  #Spoof the source ip address if you want to
    daddr = socket.inet_aton ( dest_ip )
    ihl_version = (version << 4) + ihl
    # the ! in the pack format string means network order
    ip_header = struct.pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
    packet = struct.pack(
            "!BBHHH", 8, 0, 0, 0, 0
    )
    chksum=checksum(packet)
    packet = struct.pack(
            "!BBHHH", 8, 0, chksum, 0, 0
    )
    packet=ip_header+packet
    s.sendto(packet,(ip,1))
    print "done"
    
if __name__=='__main__':
    ping('192.168.12.8')