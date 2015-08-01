#coding: utf-8
import urllib.request
import re, json

'''
http://ipinfo.io/8.8.8.8/json，return：
{
  "ip": "8.8.8.8",
  "hostname": "google-public-dns-a.google.com",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.3860,-122.0838",
  "org": "AS15169 Google Inc.",
  "postal": "94040"
}
'''
def parse_ipinfo(ip, seq):
    print("in parse_ipinfo, ip: %s, seq: %s" %(ip, seq))
    regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    regex_ip_private = re.compile('127[.]0[.]0[.]1|10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|172[.]((1[6-9])|(2\d)|(3[01]))[.]\d{1,3}[.]\d{1,3}|192[.]168[.]\d{1,3}[.]\d{1,3}')

    list_ip = regex_ip.findall(ip)
    list_ip_private = regex_ip_private.findall(ip)
    if len(list_ip) == 0:   #不为ip则返回特殊point
        print ("没有ip，返回空point")
        point = {}
        point["flag"] = 1
        point["seq"] = seq
        point["city"] = "Not known"
        point["ip"] = "*"
        point["coord"] = []
        return point
    if len(list_ip_private) > 0:
        print ("为私有ip，返回空point")
        point = {}
        point["flag"] = 1
        point["seq"] = seq
        point["city"] = "Local"
        point["ip"] = ip
        point["coord"] = []
        return point

    response = urllib.request.urlopen("http://ipinfo.io/" + ip + "/json")
    ipinfo_json = response.read().decode("utf-8")
    print("ipinfo_json : %s" %(ipinfo_json))

    ipinfo_json = json.loads(ipinfo_json)

    #hostname = ipinfo_json["hostname"] if ipinfo_json["hostname"] else "Not known"
    city = ipinfo_json["city"] if ipinfo_json["city"] else "Not known"  #
    #district = ipinfo_json["region"] if ipinfo_json["region"] else "Not known"    #
    country_name = ipinfo_json["country"] if ipinfo_json["country"] else "Not known"   #
    loc = ipinfo_json["loc"]
    coordinate_lat = re.split(',', loc)[0]  #
    coordinate_lng = re.split(',', loc)[1]  #
    #org = ipinfo_json["org"]

    print ("ip: %s " %ip)
    print ("country_name: %s" %country_name)
    #print ("district: %s" %district)
    print ("city: %s" %city)
    print ("coordinate_lat: %s" %coordinate_lat)
    print ("coordinate_lng: %s" %coordinate_lng)

    point = {}
    point["flag"] = 1
    point["seq"] = seq
    point["city"] = city
    point["ip"] = ip
    point["coord"] = [float(coordinate_lng), float(coordinate_lat)]

    return point

if __name__ == "__main__":
    parse_ipinfo("8.8.8.8", 3)