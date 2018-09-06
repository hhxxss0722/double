#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
from decimal import Decimal

class GPS:
    def deg2rad(self,d):
        return d*math.pi/180.0
    def spherical_distance(self,f1,f2,t1,t2):
        """
        根据二个经纬度换算距离
        #frompoint = [40.0351,116.40863583333334]
        #topoint = [40.0352,116.4086358333333]
        #g=GPS()
        #print g.spherical_distance(frompoint,topoint)
        """
        EARTH_RADIUS_METER =6378137.0;
        flon = self.deg2rad(f1)
        flat = self.deg2rad(f2)
        tlon = self.deg2rad(t1)
        tlat = self.deg2rad(t2)
        con = math.sin(flat)*math.sin(tlat)
        con += math.cos(flat)*math.cos(tlat)*math.cos(flon - tlon)
        return round(math.acos(con)*6378137.0/1000,4)
        
