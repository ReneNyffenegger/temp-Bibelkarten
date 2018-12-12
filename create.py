#!/usr/bin/python3
# vim: foldmethod=marker foldmarker={,}

import csv
import re


class Node():
      def __init__(self, name, lon, lat):
            self.name = name
            self.lon  = lon
            self.lat   = lat

class Way():
      def __init__(self, *nodes):
          self.nodes = nodes

class Relation():
      pass

class KML: # {
      def __init__(self):
          self.ways_to_draw  = []
          self.nodes_to_draw = []

      def draw_node(self, node, color_label, color_icon):
          if type(node) == Node:
              self.nodes_to_draw.append({'node': node, 'color_label': color_label, 'color_icon': color_icon})
          else:
              print('oha!')

      def draw_way(self, thing, color_RBGA, width): # {  RBG, not RGB!

          if type(thing) == Way:
              self.ways_to_draw.append({'way': thing, 'color': color_RBGA, 'width': width})
          else:
              print('oha!')
      # }

      def write(self, filename): # {
         kml_f = open(filename, 'w')
         self.write_intro(kml_f)

         for way_to_draw in self.ways_to_draw:
#            self.draw_way_(kml_f, way_to_draw['way'], way_to_draw['color'], way_to_draw['width'])
             self.draw_way_(kml_f, way_to_draw)

         for node_to_draw in self.nodes_to_draw:
#            self.draw_node_(kml_f, way_to_draw['way'], way_to_draw['color'], way_to_draw['width'])
             self.draw_node_(kml_f, node_to_draw)

         self.write_outro(kml_f)
      # }

      def draw_way_(self, kml_f, way): # {
#     				<name>Untitled Polygon</name>
#     		                <styleUrl>#m_ylw-pushpin</styleUrl>
          kml_f.write(
""" <Placemark>
  <Style><LineStyle><color>{:s}</color><width>{:d}</width></LineStyle></Style>
  <LineString>
    <tessellate>1</tessellate>
      <coordinates>""".format(way['color'], way['width']))

          for n in way['way'].nodes:
              kml_f.write(" {:15.12f},{:15.12f}".format(n.lon, n.lat))
      
          kml_f.write("""</coordinates>
      		</LineString>
      	</Placemark>""")
       # }

      def draw_node_(self, kml_f, node): # {
          kml_f.write(
"""<Placemark><name>{:s}</name>
  <Style><IconStyle><color>{:s}</color></IconStyle><LabelStyle><color>{:s}</color></LabelStyle></Style>
  <Point><coordinates>{:f},{:f}</coordinates></Point>
</Placemark>""".format(node['node'].name, node['color_icon'], node['color_icon'], node['node'].lon, node['node'].lat))

 
# ways['Grenze-Asser-Naphtali'] = Way(obn.Sidon, obn.Zarephath, obn.Tyre, obn.Acco)


      def write_intro(self, kml_f): # {
          # {
          kml_f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>template.kml</name>
        <!--
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
        -->
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
    way.MeerAsser       = Way(obn.Sidon, obn.Zarephath, obn.Tyre, obn.Acco)
    way.Asser_jos_19_25 = Way(obn.Helkath, obn.Hali, obn.Beten, obn.Achshaph,
                              obn.Allammelech, obn.Amad, obn.Mishal, # sie stieß an den Karmel, gegen Westen, und an den Sihor-Libnath;
                              obn.d['Beth-dagon 2'],  
                            # stieß an Sebulon und an das Tal Jiphtach-El, nördlich von Beth-Emek und Nehiel
                              obn.d['Cabul 1'],
                              obn.Ebron, obn.d['Rehob 2'], obn.Hammon, obn.d['Kanah 2'], obn.Sidon
                             )
    way.Asser_jos_19_29 = Way(obn.Hosah, obn.Ummah, obn.d['Aphek 1'], obn.d['Rehob 3'])

    way.Naphtali_jos_33 = Way(obn.Heleph, obn.Zaanannim, obn.d['Adami-nekeb'], obn.d['Jabneel 2'], obn.Lakkum)
    way.Naphtali_jos_34 = Way(obn.Lakkum, obn.d['Aznoth-tabor'], # Westwärts
                              obn.Hukkok) # Und so stieß sie an Sebulon gegen Süden, und an Asser stieß sie gegen Westen, und an Juda am Jordan gegen Sonnenaufgang.
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

        openbible_nodes[place_name] = Node(place_name, float(lon_string), float(lat_string))
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



read_openbible_merged()

create_ways()

kml = KML()

# Asser
kml.draw_way(way.MeerAsser      , 'ff0077ff', 5)
kml.draw_way(way.Asser_jos_19_25, 'ff6677ff', 5)
kml.draw_way(way.Asser_jos_19_29, 'ff5577ff', 5)

# Napthali Jos 19:33 ff {
kml.draw_way(way.Naphtali_jos_33, 'ff7711ff', 5)
kml.draw_way(way.Naphtali_jos_34, 'ff7744ff', 5)

kml.draw_node(obn.Ziddim , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Zer    , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Hammath, 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Rakkath, 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Chinnereth 2'], 'ff7711ff', 'ff7711ff')

kml.draw_node(obn.Adamah      , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Ramah 3'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Hazor 1'], 'ff7711ff', 'ff7711ff')

kml.draw_node(obn.d['Kedesh 1'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Edrei        , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['En-hazor'], 'ff7711ff', 'ff7711ff')

kml.draw_node(obn.Horem        , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Migdal-el'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Beth-anath'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Yiron         , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Beth-shemesh 3'], 'ff7711ff', 'ff7711ff')

kml.write('karte_created.kml')
# }

# Stamm_Manasse()

# write_KML_outro(kml_f)
