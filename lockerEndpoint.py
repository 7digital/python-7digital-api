#!/usr/bin/env python
"""A python interface to 7digital's locker endpoint"""
import os
from xml.dom.minidom import parseString


class Locker(object):
    def __init__(self, xml_response):
        self.xml_response = parseString(xml_response)
        
    def get_content(self):
        return self.xml_response
        
    def get_artists(self):
        results = []
        
        artist_nodes = self.xml_response.getElementsByTagName('artist')
        
        for artist_node in artist_nodes:
            print artist_node
            results.append(LockerArtist(artist_node))
            
        return results
        
class LockerArtist(object):
    def __init__(self, xml):
        self.id = xml.getAttribute('id')
        self.name = self.__extract(xml, 'name')
        self.url = self.__extract(xml, 'url')
    
    def __extract(self, node, name, index = 0):
        """Extracts a value from the xml string"""
        try:
            nodes = node.getElementsByTagName(name)
            
            if len(nodes):
                if nodes[index].firstChild:
                    return nodes[index].firstChild.data.strip()
                else:
                    return None
        except:
            return None
        
        
