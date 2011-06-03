#!/usr/bin/env python
"""A python interface to 7digital's locker endpoint"""
import os
import urllib2, urllib
import re
import urlparse
from xml.dom import minidom


class Locker(object):
    def __init__(self, xml_response):
        self.xml_response = xml_response
        
    def get_release(self):
        return self.xml_response

def get_user_locker(xml_response):
	return Locker(xml_response)
        
        
