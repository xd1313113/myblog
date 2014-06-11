'''
Created on May 30, 2014

@author: di
'''
import urllib
import urllib2
import six
import json

class flickrImage:
    
    def __init__(self,*args, **kwds):
        self.farm = kwds['farm']
        self.id = kwds['id']
        self.isfamily = kwds['isfamily']
        self.isfriend = kwds['isfriend']
        self.ispublic = kwds['ispublic']
        self.owner = kwds['owner']
        self.secret = kwds['secret']
        self.server = kwds['server']
        self.title = kwds['title']
        self.found = False
        
    def get_pic_url(self, size='o'):      
#         s    small square 75x75
#         q    large square 150x150
#         t    thumbnail, 100 on longest side
#         m    small, 240 on longest side
#         n    small, 320 on longest side
#         -    medium, 500 on longest side
#         z    medium 640, 640 on longest side
#         c    medium 800, 800 on longest side
#         b    large, 1024 on longest side*
#         o    original image, either a jpg, gif or png, depending on source format
        if size == 'o':
            return "http://farm%s.staticflickr.com/%s/%s_%s_o.%s" % (self.farm, self.server, self.id, self.originalsecret, self.originalformat)
        else:
            return "http://farm%s.staticflickr.com/%s/%s_%s_%s.jpg" % (self.farm, self.server, self.id, self.secret, size)

class Flickr:
    '''
    classdocs
    '''


    def __init__(self, apikey):
        '''
        Constructor
        '''
        self.key = apikey
        self.flickrHost = "https://api.flickr.com/services/rest/"
        
    def search(self, *args, **kwds):
        
        kwds["format"] = "json"
        kwds["api_key"] = self.key
        kwds["method"] ="flickr.photos.search"
        postdata = urllib.urlencode(kwds)
        response = urllib2.urlopen(self.flickrHost, postdata)
        data = response.read()
        response.close()
        data = data[14:-1]
        
        jsonimages = self.parse_json(data)
        
        jsonimages = jsonimages['photos']['photo']
        images = []
        for o in jsonimages:
            newImage = flickrImage(id = o['id'],
                                farm = o['farm'],
                                isfamily = o['isfamily'],
                                isfriend = o['isfriend'],
                                ispublic = o['ispublic'],
                                owner = o['owner'],
                                secret = o['secret'],
                                server = o['server'],
                                title = o['title']
                                )
            #newImage = self.getImageInfo(newImage.id, newImage)
            images.append(newImage)
        
        return images
        
        
    def parse_json(self, json_string):
        '''Parses a JSON response from Flickr.'''

        if isinstance(json_string, six.binary_type):
            json_string = json_string.decode('utf-8')


        return json.loads(json_string)

    
    def getImageInfo(self,photo_id,image):
        urldata = {}
        urldata["format"] = "json"
        urldata["api_key"] = self.key
        urldata["method"] ="flickr.photos.getInfo"
        urldata["photo_id"] = photo_id
        postdata = urllib.urlencode(urldata)
        response = urllib2.urlopen(self.flickrHost, postdata)
        data = response.read()
        response.close()
        data = data[14:-1]
        jsonimage = self.parse_json(data)
        
        try:
            code  = jsonimage['code']
            image.found = False
            return image
        except:
            image.found = True
            image.description = jsonimage['photo']['description']['_content']
#            print jsonimage['photo']['dates']['taken']
            image.taken = jsonimage['photo']['dates']['taken']
            image.comments = jsonimage['photo']['comments']['_content']
            image.tags = jsonimage['photo']['tags']['tag']
            image.originalsecret = jsonimage['photo']['originalsecret']
            image.originalformat = jsonimage['photo']['originalformat']
            
            return image
            
        

        