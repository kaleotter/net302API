import json
import urllib3
import random
import string


class GMapsAddressConverter:
    

    
    def to_coords(address_1, address_2, address_3, city, postcode):
        
        
        longaddress=address_1+',+'
        
        if address_2 != '':
            longaddress+= address_2 + ',+'
            
        if address_3 !='':
            longaddress += address_3+ ',+'
            
        longaddress += city
        longaddress = longaddress.replace(" ","+")
            
        apikey='AIzaSyC-hE-Yq3JEqvgx6qzLHbbbAhgUQMWK4oI'
        http = urllib3.PoolManager()
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address='
                       + longaddress+ '&key='+apikey)
        print(url)
        request = http.request('GET', url)
        print("request made")
          
        if request.status == 200:
            
            print("here is the request")
            print(request.data)
            data = json.loads(request.data)
            
            lat= data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            
            print(lat)
            print(lng)
            returndata={'lat':lat, 'lng':lng}
            
            return (returndata)
        
        else:
            return (request.status)
        
        
    def to_address(self, lat, lng):
        'do the thing'
        return (False)
        

class RandomStringGen ():
    
    def generate(size=8, chars=string.ascii_uppercase+string.digits):
        
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
        