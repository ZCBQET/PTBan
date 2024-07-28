from urllib.parse import quote
import requests
import bencodepy
import hashlib
import string
import random
import uuid

torrent_path = input("种子：").replace("\"","")
with open(torrent_path, 'rb') as f:
    torrent_data = f.read()
    decoded_data = bencodepy.decode(torrent_data)
    tracker = decoded_data[b'announce']
    
    info = decoded_data[b'info']
    files = info[b'files']
    size = 0
    for file in files:
        size+= file[b'length']
    
    info = bencodepy.encode(info)
    sha1 = hashlib.sha1()
    sha1.update(info)
    info_hash = quote(sha1.digest())

    url = tracker.decode('utf-8')
    url += "&info_hash=" + info_hash
    url += "&peer_id=-qB4390-" + (''.join(random.choices(string.ascii_letters + string.digits, k=12)))
    url += "&port=" + str(random.randint(10000,65535))
    url += "&uploaded=0"
    url += "&downloaded=18446744073709551616" #16384PB=18446744073709551616Bytes
    url += "&left=" + str(size)
    url += "&corrupt=0"
    url += "&key=" + uuid.uuid4().hex[:8].upper()
    url += "&event=started"
    url += "&numwant=200"
    url += "&compact=1"
    url += "&no_peer_id=1"
    url += "&supportcrypto=1"
    url += "&redundant=0"
    
    #print(url)
    response = requests.get(url,headers = {'User-Agent' : 'qBittorrent/4.3.9'})
    print(response.text)
    
    
    
