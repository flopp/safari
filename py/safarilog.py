#!/usr/bin/env python3

import re
import dateutil.parser


class SafariLog:
    _uuid = None
    _internal_id = None
    _type = None
    _date = None
    _user = None
    _user_url = None
    _comment = None
    _coordinates = None
    _images = None

    def load_from_json(self, json_data):
        self._uuid = json_data['uuid']
        self._internal_id = json_data['internal_id']
        self._type = json_data['type']
        self._date = dateutil.parser.parse(json_data['date'])
        self._user = json_data['user']['username']
        self._user_url = json_data['user']['profile_url']
        self._comment = json_data['comment']
        self._images = json_data['images']
        self.determine_coordinates()
        self.fix_urls()

    def determine_coordinates(self):
        self._coordinates = None
        text = self._comment.lower()
        text = re.sub(r'<[^>]*>', " ", text)
        text = text.replace(",", ".")
        text = re.sub(r'\s*\.\s*', '.', text)
        text = re.sub(r'&[^&;];', " ", text)
        text = text.replace("&deg;", " ")
        tt = ""

        last_space = True
        for c in text:
            if c.isalnum() or c == ".":
                tt += c
                last_space = False
            elif c == "o":
                tt += "e"
                last_space = False
            elif not last_space:
                tt += " "
                last_space = True
        text = tt

        try:
            hdms_re = r'([ns])\s*(\d+)\s+(\d+)\s+(\d[\d\.]*)\s*([ew])\s*(\d+)\s+(\d+)\s+(\d[\d\.]*)'
            hdm_re = r'([ns])\s*(\d+)\s+(\d[\d\.]*)\s*([ew])\s*(\d+)\s+(\d[\d\.]*)'
            hd_re = r'([ns])\s*(\d[\d\.]*)\s*([ew])\s*(\d[\d\.]*)'

            m = re.search(hdms_re, text)
            if m:
                self._coordinates = self.parse_hdms(m.groups())
                if self._coordinates:
                    return
            m = re.search(hdm_re, text)
            if m:
                self._coordinates = self.parse_hdm(m.groups())
                if self._coordinates:
                    return
            m = re.search(hd_re, text)
            if m:
                self._coordinates = self.parse_hd(m.groups())
                if self._coordinates:
                    return
        except ValueError as e:
            print(e)
            print(text)
            print(self._comment)
            return
    
    def fix_urls(self):
        self._user_url = re.sub(r'^http:', "https:", self._user_url)
        for img in self._images:
            img['url'] = re.sub(r'^http:', "https:", img['url'])
            img['thumb_url'] = re.sub(r'^http:', "https:", img['thumb_url'])
    
    @staticmethod
    def to_float(s):
        s2 = ""
        dot = False
        for c in s:
            if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                s2 += c
            elif not dot:
                s2 += "."
                dot = True
        s2.rstrip(".")
        return float(s2)

    def parse_hdms(self, hdms):
        # N DD MM SS E DD MM SS
        lat = self.to_float(hdms[1]) + self.to_float(hdms[2])/60.0 + self.to_float(hdms[3])/3600.0
        if hdms[0] == "s":
            lat = -lat
        lng = self.to_float(hdms[5]) + self.to_float(hdms[6])/60.0 + self.to_float(hdms[7])/3600.0
        if hdms[4] == "w":
            lng = -lng
        if self.validate_coords(lat, lng):
            return "{}|{}".format(lat, lng)
        else:
            return None

    def parse_hdm(self, hdm):
        # N DD MM E DD MM
        lat = self.to_float(hdm[1]) + self.to_float(hdm[2])/60.0
        if hdm[0] == "s":
            lat = -lat
        lng = self.to_float(hdm[4]) + self.to_float(hdm[5])/60.0
        if hdm[3] == "w":
            lng = -lng
        if self.validate_coords(lat, lng):
            return "{}|{}".format(lat, lng)
        else:
            return None

    def parse_hd(self, hd):
        # N DD E DD
        lat = self.to_float(hd[1])
        if hd[0] == "s":
            lat = -lat
        lng = self.to_float(hd[3])
        if hd[2] == "w":
            lng = -lng
        if self.validate_coords(lat, lng):
            return "{}|{}".format(lat, lng)
        else:
            return None

    @staticmethod
    def validate_coords(lat, lng):
        return -90 <= lat <= 90 and -180 <= lng <= 180

    def to_string(self):
        return u"{0}: {1}, {2}".format(self._user, self._date, self._coordinates)


def load_logs(json_array):
    logs = []
    for item in json_array:
        log = SafariLog()
        log.load_from_json(item)
        logs.append(log)
    return logs
