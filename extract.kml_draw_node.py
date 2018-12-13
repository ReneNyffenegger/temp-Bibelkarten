#!/usr/bin/python3

import csv
import re

seen = {}

for ch in range(13, 20):
    for v in range(1, 99):

        merged_f   = open('openbible.info/merged.txt', 'r')
        merged_csv = csv.reader(merged_f, delimiter="\t")
        
        next(merged_f, None)
        next(merged_f, None)
        
        for record in merged_csv:
        
            lat_string = record[2]
            lon_string = record[3]
        
            if lon_string == '?' or lat_string == '?':
               continue
        
            notes = record[4]

            v_txt = 'Josh ' + str(ch) + ':' + str(v)

            if re.search('\\b' + v_txt + '\\b', notes):
                place_name = record[0]

                if place_name in seen:
                   continue

                seen[place_name] = 1
                   

                if re.search('[ -]', place_name):
                   print("kml.draw_node(obn.d['" + place_name + "'] , 'ffffffff', 'ffffffff') # " + v_txt)
                else:
                   print("kml.draw_node(obn." + place_name + ", 'ffffffff', 'ffffffff') # " + v_txt)



#           print(notes)
        
     
        merged_f.close()
