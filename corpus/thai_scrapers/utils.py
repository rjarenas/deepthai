# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:20:05 2020

@author: Ruben
"""
import re

def contains_thai(str):
    # Regex string representing unicode Thai 
    regex = r"([\u0E00-\u0E7F]+)"
    pattern = re.compile(regex)
    
    return len(pattern.findall(str)) > 0

