#!/usr/bin/env python
"""A python interface to 7digital's locker endpoint"""
import os
from xml.dom.minidom import parseString


class Locker(object):
    def __init__(self, xml_response):
        self.xml_response = parseString(xml_response)
        
    def get_contents(self):
        results = []
        locker_items = self.xml_response.getElementsByTagName('lockerRelease')
        
        for item in locker_items:
            results.append(LockerItem(item))
            
        return results
        
    def get_artists(self):
        results = []
        artist_nodes = self.xml_response.getElementsByTagName('artist')
        
        for artist in artist_nodes:
            results.append(LockerArtist(artist))
            
        return results
    
    def get_releases(self):
        results = []
        release_nodes = self.xml_response.getElementsByTagName('release')
        for release in release_nodes:
            results.append(LockerRelease(release))
        
        return results
        
    def get_tracks(self):
        results = []
        track_nodes = self.xml_response.getElementsByTagName('lockerTrack')
        for track in track_nodes:
            results.append(LockerTrack(track))
        
        return results

class _LockerBase(object):
    def extract(self, node, name, index = 0):
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

class LockerItem(_LockerBase):
    def __init__(self, xml):
        self.release = LockerRelease(xml.getElementsByTagName('release')[0])
        self.tracks = self.__get_release_tracks(xml.getElementsByTagName('lockerTrack'))
        
    def __get_release_tracks(self, tracks):
        result = []
        for track in tracks:
            result.append(LockerTrack(track))
        return result
            
class LockerTrack(_LockerBase):
    def __init__(self, xml):
        self.track = Track(xml.getElementsByTagName('track')[0])
        self.remaining_downloads = self.extract(xml, 'remainingDownloads') 
        self.purchaseDate = self.extract(xml, 'purchaseDate') 
        self.download_urls = self.__get_download_urls(xml.getElementsByTagName('downloadUrls'))
    
    def __get_download_urls(self, urls):
        result = []
        for url in urls:
            result.append(DownloadUrls(url))
        return result

class DownloadUrls(_LockerBase):
    def __init__(self, xml):
        self.url = self.extract(xml, 'url')
        self.format = Format(xml.getElementsByTagName('format')[0])

class Format(_LockerBase):
    def __init__(self, xml):
        self.id = xml.getAttribute('id')
        self.file_format = self.extract(xml, 'fileFormat')
        self.bit_rate = self.extract(xml, 'bitRate')
        
class Track(_LockerBase):
    def __init__(self, xml):
        self.id = xml.getAttribute('id')
        self.title = self.extract(xml, 'title')
        self.version = self.extract(xml, 'version')
        self.artist = LockerArtist(xml.getElementsByTagName('artist')[0])
        self.url = self.extract(xml, 'url')
        
class LockerRelease(_LockerBase):
    def __init__(self, xml):
        self.id = xml.getAttribute('id')
        self.title = self.extract(xml, 'title') 
        self.type = self.extract(xml, 'type')
        self.artist = LockerArtist(xml.getElementsByTagName('artist')[0])
        self.url = self.extract(xml, 'url')
        self.image = self.extract(xml, 'image')
        self.release_date = self.extract(xml, 'releaseDate')
        
class LockerArtist(_LockerBase):
    def __init__(self, xml):
        self.id = xml.getAttribute('id')
        self.name = self.extract(xml, 'name')
        self.url = self.extract(xml, 'url')
    
        
