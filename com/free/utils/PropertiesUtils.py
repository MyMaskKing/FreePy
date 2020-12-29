# coding=UTF-8
'''
Created on 2020年4月11日

@author: dapao
'''
import re
import os
import tempfile
"""
※重要：共通方法的导入
"""
from com.free.constant import CommonConstants

class PropertiesUtils:
    
    file_name = CommonConstants.DEFAULT_CONFIG_PATH
    
    def __init__(self):
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r', encoding=CommonConstants.ENCODING_UTF8)
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=', 1)
                    self.properties[strs[0].strip()] = strs[1].strip()
        finally:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key):
        if key in self.properties:
            return self.properties[key]
        return CommonConstants.EMPTY

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            tmpfile.write(line)
        if not found and append_on_not_exists:
            tmpfile.write('\n' + to_str)
        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content)
        w_open.close()

        tmpfile.close()
    else:
        print( "file %s not found",file_name)