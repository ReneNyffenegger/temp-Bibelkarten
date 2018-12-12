#!/usr/bin/python3
# vim: foldmethod=marker foldmarker={,}

import csv
import re


class Node():
      def __init__(self, lon, lat):
            self.lon = lon
            self.lat = lat

class Way():
      def __init__(self, *nodes):
          self.nodes = nodes

class Relation():
      pass

class KML: # {
      def __init__(self):
          self.ways_to_draw = []

      def draw(self, thing, color_RBGA, width): # {  RBG, not RGB!

          if type(thing) == Way:
              self.ways_to_draw.append({'way': thing, 'color': color_RBGA, 'width': width})
          else:
              print('oha!')
      # }

      def write(self, filename): # {
         kml_f = open(filename, 'w')
         self.write_intro(kml_f)

         for way_to_draw in self.ways_to_draw:
             self.draw_way(kml_f, way_to_draw['way'], way_to_draw['color'], way_to_draw['width'])

         self.write_outro(kml_f)
      # }

      def draw_way(self, kml_f, way, color, width): # {
#     				<name>Untitled Polygon</name>
#     		                <styleUrl>#m_ylw-pushpin</styleUrl>
          kml_f.write(
""" <Placemark>
  <Style><LineStyle><color>{:s}</color><width>{:d}</width></LineStyle></Style>
  <LineString>
    <tessellate>1</tessellate>
      <coordinates>""".format(color, width))
          for n in way.nodes:
              kml_f.write(" {:15.12f},{:15.12f}".format(n.lon, n.lat))
      
          kml_f.write("""</coordinates>
      		</LineString>
      	</Placemark>""")
       # }

 
# ways['Grenze-Asser-Naphtali'] = Way(obn.Sidon, obn.Zarephath, obn.Tyre, obn.Acco)


      def write_intro(self, kml_f): # {
          # {
          kml_f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>template.kml</name>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
	<StyleMap id="msn_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_ylw-pushpin</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sh_ylw-pushpin">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
		</LineStyle>
		<PolyStyle>
			<color>ab7faaff</color>
		</PolyStyle>
	</Style>
	<Style id="sn_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
		</LineStyle>
		<PolyStyle>
			<color>ab7faaff</color>
		</PolyStyle>
	</Style>
""") # }
          return kml_f
     # }

      def write_outro(self, kml_f): # {
          kml_f.write("""
      </Document>
      </kml>""")
      # }
# }              

class AddDotAccessToDict: # {
#     d = dict()
#     __getattr__ = dict.get
#     __setattr__ = dict.__setitem__
#     __delattr__ = dict.__delitem__

      def __init__(self, d):
          self.d = d

      def __getattr__(self, attr):
          return self.d[attr]

      def __setattr__(self, attr, val):
#         if attr == 'd':
          object.__setattr__(self, attr, val)
#            return
#         self.d[attr] = val

# }

openbible_nodes = {}
obn = AddDotAccessToDict(openbible_nodes)
ways = {};
way = AddDotAccessToDict(ways)

def create_ways(): # {
    way.MeerAsser = Way(obn.Sidon, obn.Zarephath, obn.Tyre, obn.Acco)
# }


def read_openbible_merged(): # {

    merged_f   = open('openbible.info/merged.txt', 'r')
    merged_csv = csv.reader(merged_f, delimiter="\t")

    next(merged_f, None)
    next(merged_f, None)

    for record in merged_csv:

        lat_string = record[2]
        lon_string = record[3]

        if lon_string == '?' or lat_string == '?':
           continue

        place_name = record[0]
        if place_name in openbible_nodes:
           print('Place name {:s} already seen'.format(place_name))

        lon_string = re.sub('[<~>?]', '', lon_string)
        lat_string = re.sub('[<~>?]', '', lat_string)

        if lon_string == '' or lat_string == '':
           continue

        openbible_nodes[place_name] = Node(float(lon_string), float(lat_string))
#       openbible_nodes[place_name]['lat'] = lat
#       openbible_nodes[place_name]['lon'] = lon

# }

def kml_start_folder(kml_f, name): # {
    kml_f.write('<Folder><name>{:s}</name><open>1</open>'.format(name))
# }

def kml_end_folder(kml_f): # {
    kml_f.write('</Folder>')
# }

def Stamm_Manasse(): # {
    kml_start_folder(kml_f, 'Stamm Manasse')
    kml_end_folder(kml_f)
# }



# kml_f = write_intro()

# # {
# kml_f.write("""
# 	<Folder>
# 		<name>Karte</name>
# 		<open>1</open>
# 		<Folder>
# 			<name>Folder</name>
# 			<open>1</open>
# 			<Placemark>
# 				<name>Mit Text</name>
# 				<description>Das ist der Text</description>
# 				<LookAt>
# 					<longitude>34.68136420025282</longitude>
# 					<latitude>31.92449253083083</latitude>
# 					<altitude>0</altitude>
# 					<heading>2.685299478742767</heading>
# 					<tilt>0</tilt>
# 					<range>310883.4302136681</range>
# 					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
# 				</LookAt>
# 				<styleUrl>#m_ylw-pushpin</styleUrl>
# 				<Point>
# 					<gx:drawOrder>1</gx:drawOrder>
# 					<coordinates>34.68136420025282,31.92449253083082,0</coordinates>
# 				</Point>
# 			</Placemark>
# 			<Placemark>
# 				<name>Nur Name</name>
# 				<LookAt>
# 					<longitude>34.68136430383336</longitude>
# 					<latitude>31.92449231718748</latitude>
# 					<altitude>0</altitude>
# 					<heading>2.685299533516287</heading>
# 					<tilt>0</tilt>
# 					<range>310883.4370406983</range>
# 					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
# 				</LookAt>
# 				<styleUrl>#m_ylw-pushpin</styleUrl>
# 				<Point>
# 					<gx:drawOrder>1</gx:drawOrder>
# 					<coordinates>34.93028888043367,31.980195320258,0</coordinates>
# 				</Point>
# 			</Placemark>
# 			<Placemark>
# 				<name>Untitled Placemark</name>
# 				<LookAt>
# 					<longitude>34.99944376518829</longitude>
# 					<latitude>31.74595123838236</latitude>
# 					<altitude>0</altitude>
# 					<heading>2.845835834057495</heading>
# 					<tilt>0</tilt>
# 					<range>203700.8230242897</range>
# 					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
# 				</LookAt>
# 				<styleUrl>#m_ylw-pushpin</styleUrl>
# 				<Point>
# 					<gx:drawOrder>1</gx:drawOrder>
# 					<coordinates>34.99944376518828,31.74595123838236,0</coordinates>
# 				</Point>
# 			</Placemark>
# 			<Placemark>
# 				<name>Untitled Polygon</name>
# 				<styleUrl>#msn_ylw-pushpin</styleUrl>
# 				<Polygon>
# 					<tessellate>1</tessellate>
# 					<outerBoundaryIs>
# 						<LinearRing>
# 							<coordinates>
# 								35.01906060229162,31.78598741605257,0 34.97883498742767,32.01432008475683,0 34.71162012253016,31.93428660128429,0 35.01906060229162,31.78598741605257,0 
# 							</coordinates>
# 						</LinearRing>
# 					</outerBoundaryIs>
# 				</Polygon>
# 			</Placemark>
# 		</Folder>
# 	</Folder>
# 
# """) # }


read_openbible_merged()

create_ways()

kml = KML()

kml.draw(way.MeerAsser, 'ff0077ff', 5)

kml.write('karte_created.kml')

# Stamm_Manasse()

# write_KML_outro(kml_f)
