#!/usr/bin/python3
# vim: foldmethod=marker foldmarker={,}

import csv
import re


def deg(degrees, minutes, seconds):
    return degrees + minutes/60  + seconds/3600

class Node(): # {
      def __init__(self, name, lon, lat):
            self.name        = name
            self.lon         = lon
            self.lat         = lat
            self.description = None
            
      def writeCoordinatePairToKML(self, kml_f):
          kml_f.write(" {:15.12f},{:15.12f}".format(self.lon, self.lat))
      
      def __eq__(self, other):
          return self.name == other.name
# }

class Way(): # {
      def __init__(self, *nodes):
          self.nodes = nodes
      
      def setName(self, name):
          self.name = name

      def writeCoordinatePairsToKML(self, kml_f): # {
          for n in self.nodes:
              n.writeCoordinatePairToKML(kml_f)
# qqq         kml_f.write(" {:15.12f},{:15.12f}".format(n.lon, n.lat))

      # }
# }


#  class Ways():
#        pass

# class Relation():
#       def __init__(self, *things):
#           self.things = things


class KML: # {

      class BalloonStyle: # {
            def __init__(self, id):
                self.id   = id 
                self.text = '$[description]' # This seems to be a reasonable default.

      # }

      def __init__(self): # {
          self.ways_to_draw  = []
          self.nodes_to_draw = []
          self.areas_to_draw = []
          self.balloonStyles = []
      # }

      def draw_node(self, node, color_label, color_icon): # {
          if type(node) == Node:
              self.nodes_to_draw.append({'node': node, 'color_label': color_label, 'color_icon': color_icon})
          else:
              print('oha!')
      # }

      def draw_way(self, thing, color_ABGR, width): # { 

          if type(thing) == Way:
              self.ways_to_draw.append({'way': thing, 'color': color_ABGR, 'width': width})
          else:
              print('oha!')
      # }

      def draw_area(self, name, colorBorder, widthBorder, colorArea, ways_or_nodes): # {
          self.areas_to_draw.append({'name': name, 'ways_or_nodes': ways_or_nodes, 'colorBorder': colorBorder, 'widthBorder': widthBorder, 'colorArea': colorArea})
      # }

      def addBalloonStyle(self, id): # {
          ballonStyle = KML.BalloonStyle(id)
          self.balloonStyles.append(ballonStyle)
          return ballonStyle

      # }

      def write(self, filename): # {
         kml_f = open(filename, 'w')
         self.write_intro(kml_f)

         for ballon_style in self.balloonStyles:
             self.draw_ballon_style(kml_f, ballon_style)

         for area in self.areas_to_draw: # {
             self.draw_area_(kml_f, area)
         # }

         for way_to_draw in self.ways_to_draw:
             self.draw_way_(kml_f, way_to_draw)

         for node_to_draw in self.nodes_to_draw:
             self.draw_node_(kml_f, node_to_draw)

         self.write_outro(kml_f)
      # }

      def writePlacemarkIntro(self, kml_f, name): # {
          kml_f.write('<Placemark><name>{:s}</name>'.format(name))
      # }

      def writeLineStyle(self, kml_f, color, width): # {
          kml_f.write('<LineStyle><color>{:s}</color><width>{:f}</width></LineStyle>'.format(color, width))
      # }

      def writeLinearRing(self, kml_f, ways_or_nodes): # {

          kml_f.write('<LinearRing><coordinates>')

          firstNode = ways_or_nodes[0]

#         print(len(ways_or_nodes))

          way_or_node_cnt = 0
          for way_or_node in ways_or_nodes:
              way_or_node_cnt += 1

              if type(way_or_node) == Node:
                 way_or_node.writeCoordinatePairToKML(kml_f)
              else:
                 way_or_node.writeCoordinatePairsToKML(kml_f)

              firstNode.writeCoordinatePairsToKML(kml_f)



          kml_f.write('</coordinates></LinearRing>')


      # }

      def draw_ballon_style(self, kml_f, ballon_style):
          kml_f.write('<Style id="' + ballon_style.id + '"><BalloonStyle>')

          kml_f.write('<text>' + ballon_style.text + '</text>')
          kml_f.write('</BalloonStyle></Style>')

      def draw_area_(self, kml_f, area): # {
          self.writePlacemarkIntro(kml_f, area['name'])
          kml_f.write('<Style>')
          self.writeLineStyle(kml_f, area['colorBorder'], area['widthBorder'])
          kml_f.write('<PolyStyle><color>{:s}</color></PolyStyle>'.format(area['colorArea']))
          kml_f.write('</Style>')

          kml_f.write("""
    <Polygon>
      <tessellate>1</tessellate>
      <outerBoundaryIs>""")

          self.writeLinearRing(kml_f, area['ways_or_nodes'])

          kml_f.write(""" </outerBoundaryIs>
    </Polygon>""")

          kml_f.write('</Placemark>')
      # }

      def draw_way_(self, kml_f, way): # {
          kml_f.write(
""" <Placemark><name>{:s}</name>
  <Style><LineStyle><color>{:s}</color><width>{:d}</width></LineStyle></Style>
  <LineString>
    <tessellate>1</tessellate>
      <coordinates>""".format(way['way'].name, way['color'], way['width']))

          way['way'].writeCoordinatePairsToKML(kml_f)

#           for n in way['way'].nodes:
#               n.writeCoordinatePairToKML(kml_f)
# # qqq         kml_f.write(" {:15.12f},{:15.12f}".format(n.lon, n.lat))
#       
          kml_f.write("""</coordinates>
      		</LineString>
      	</Placemark>""")
       # }

      def draw_node_(self, kml_f, node): # {
          self.writePlacemarkIntro(kml_f, node['node'].name)
          kml_f.write("""
  <Style>
    <IconStyle>
      <color>{:s}</color>
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
      </Icon>
    </IconStyle><LabelStyle><color>{:s}</color></LabelStyle></Style>""".format(node['color_icon'], node['color_icon']))

          if node['node'].description:
             kml_f.write('<description>{:s}</description><StyleUrl>#note</StyleUrl>'.format(node['node'].description))

          kml_f.write("<Point><coordinates>")

          node['node'].writeCoordinatePairToKML(kml_f)

          # <coordinates>{:f},{:f}</coordinates>
          kml_f.write("""</coordinates></Point>
</Placemark>""") # .format(node['node'].name, node['color_icon'], node['color_icon'], node['node'].lon, node['node'].lat))
       # }
 
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
          if type(val) == Way:
             val.setName(attr)
#            return
#         self.d[attr] = val

# }

openbible_nodes = {}
tq84_nodes      = {}
obn = AddDotAccessToDict(openbible_nodes)
tqn = AddDotAccessToDict(tq84_nodes)
ways = {};
way = AddDotAccessToDict(ways)

# tq84 nodes {

def addTQ84Node(name, lon_deg, lon_min, lon_sec, lat_deg, lat_min, lat_sec):
    tq84_nodes[name] = Node(name, deg(lon_deg, lon_min, lon_sec), deg(lat_deg, lat_min, lat_sec))

#                                  East              North
addTQ84Node('SalzmeerSued'     ,   35, 23,  4.67,    30, 55, 41.19)
addTQ84Node('Hezron'           ,   34, 40, 55.94,    30, 53, 49.65)
addTQ84Node('BachAegypten_Meer',   33, 49, 44.55,    31,  9, 14.32)

# }

def create_ways(): # {
    way.MeerAsser       = Way(obn.Sidon, obn.Zarephath, obn.Tyre, obn.Acco)
    way.Meer_Asdod_Gaza = Way(obn.Ashdod, obn.Ashkelon, obn.Gaza)

    way.Grenze_Philister_jos_13_2 = Way(obn.Ashdod, obn.Ekron, obn.Gath, obn.Shihor, obn.Gaza)

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

# def create_areas():
#     area.alle_Bezirke_der_Phlister_und_das_ganze_Geschuri=Area(way.Meer_Asdod_Gaza, obn.Ekron, obn.Gath, obn.Shihor)
#     pass

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

# descriptions {

obn.Akrabbim.description = "Nahe Grenze zu Edom? (Jos 15:1<br/>An Grenze der Amoriter (Ri 1:36)"

# }

create_ways()

kml = KML()


color_label_river = 'ffff6666'
color_label_icon  = 'ffff0000'

balloonStyleNote = kml.addBalloonStyle('note')

# def alle_Bezirke_der_Phlister_und_das_ganze_Geschuri:

# Jos 13 {


# alle Bezirke der Philister und das ganze Geschuri; {
kml.draw_node(obn.Ashdod  , 'ff000000', 'ff000000') # Josh 13:3
kml.draw_node(obn.Ashkelon, 'ff000000', 'ff000000') # Josh 13:3
kml.draw_node(obn.Egypt   , 'ff000000', 'ff000000') # Josh 13:3
kml.draw_node(obn.Ekron   , 'ff000000', 'ff000000') # Josh 13:3
kml.draw_node(obn.Gath    , 'ff000000', 'ff000000') # Josh 13:3
kml.draw_node(obn.Gaza    , 'ff000000', 'ff000000') # Josh 13:3

kml.draw_node(obn.Shihor  , color_label_river, color_label_icon) # Josh 13:3

kml.draw_area('Philister und Bezirke des Geschurri', '00000000', 0, 'c0000000', (way.Meer_Asdod_Gaza, way.Grenze_Philister_jos_13_2))

# }

kml.draw_node(obn.d['Aphek 1'] , 'ffffffff', 'ffffffff') # Josh 13:4

kml.draw_node(obn.Mearah, 'ffffffff', 'ffffffff') # Josh 13:4

kml.draw_node(obn.d['Baal-gad'] , 'ffffffff', 'ffffffff') # Josh 13:5
kml.draw_node(obn.Lebanon, 'ffffffff', 'ffffffff') # Josh 13:5
kml.draw_node(obn.d['Lebo-hamath'] , 'ffffffff', 'ffffffff') # Josh 13:5
kml.draw_node(obn.d['Mount Hermon'] , 'ffffffff', 'ffffffff') # Josh 13:5
kml.draw_node(obn.d['Misrephoth-maim'] , 'ffffffff', 'ffffffff') # Josh 13:6
# kml.draw_node(obn.Jordan, 'ffffffff', 'ffffffff') # Josh 13:8
kml.draw_node(obn.d['Aroer 1'] , color_label_river, color_label_icon) # Josh 13:9
kml.draw_node(obn.d['Dibon 1'] , 'ffffffff', 'ffffffff') # Josh 13:9
kml.draw_node(obn.Medeba, 'ffffffff', 'ffffffff') # Josh 13:9
kml.draw_node(obn.d['Valley of the Arnon'] , 'ffffffff', 'ffffffff') # Josh 13:9
kml.draw_node(obn.Heshbon              , 'ffff7744', 'ffff7744') # Josh 13:10
kml.draw_node(obn.Bashan               , 'ffff7744', 'ffff7744') # Josh 13:11
kml.draw_node(obn.Gilead               , 'ffff7744', 'ffff7744') # Josh 13:11
kml.draw_node(obn.Salecah              , 'ffff7744', 'ffff7744') # Josh 13:11
kml.draw_node(obn.Edrei                , 'ffff7744', 'ffff7744') # Josh 13:12
# kml.draw_node(obn.Geshur             , 'ffffffff', 'ffffffff') # Josh 13:13
# kml.draw_node(obn.Maacath            , 'ffffffff', 'ffffffff') # Josh 13:13

# Ruben {


col_ruben_label = 'ff44ff66'
col_ruben_icon  = 'ff44ff66' 
kml.draw_node(obn.d['Bamoth-baal']     , col_ruben_label, col_ruben_icon) # Josh 13:17
kml.draw_node(obn.d['Beth-baal-meon']  , col_ruben_label, col_ruben_icon) # Josh 13:17
kml.draw_node(obn.Jahaz                , col_ruben_label, col_ruben_icon) # Josh 13:18
kml.draw_node(obn.Kedemoth             , col_ruben_label, col_ruben_icon) # Josh 13:18
kml.draw_node(obn.Mephaath             , col_ruben_label, col_ruben_icon) # Josh 13:18
kml.draw_node(obn.d['Kiriathaim 1']    , col_ruben_label, col_ruben_icon) # Josh 13:19
kml.draw_node(obn.Sibmah               , col_ruben_label, col_ruben_icon) # Josh 13:19
kml.draw_node(obn.d['Zereth-shahar']   , col_ruben_label, col_ruben_icon) # Josh 13:19
kml.draw_node(obn.d['Beth-peor']       , col_ruben_label, col_ruben_icon) # Josh 13:20
kml.draw_node(obn.d['Beth-jeshimoth']  , col_ruben_label, col_ruben_icon) # Josh 13:20
kml.draw_node(obn.Pisgah               , col_ruben_label, col_ruben_icon) # Josh 13:20
kml.draw_node(obn.Midian               , col_ruben_label, col_ruben_icon) # Josh 13:21

# }
# Gad {

col_gad_label = 'ffff4466'
col_gad_icon  = 'ffff4466'

kml.draw_node(obn.d['Aroer 2'] , col_gad_label, col_gad_icon) # Josh 13:25
kml.draw_node(obn.Jazer  , col_gad_label, col_gad_icon) # Josh 13:25
kml.draw_node(obn.Rabbah , col_gad_label, col_gad_icon) # Josh 13:25
kml.draw_node(obn.Betonim, col_gad_label, col_gad_icon) # Josh 13:26
kml.draw_node(obn.d['Debir 3'] , col_gad_label, col_gad_icon) # Josh 13:26
kml.draw_node(obn.Mahanaim, col_gad_label, col_gad_icon) # Josh 13:26
kml.draw_node(obn.d['Ramath-mizpeh'] , col_gad_label, col_gad_icon) # Josh 13:26
kml.draw_node(obn.d['Beth-haram'] , col_gad_label, col_gad_icon) # Josh 13:27
kml.draw_node(obn.d['Beth-nimrah'] , col_gad_label, col_gad_icon) # Josh 13:27
kml.draw_node(obn.d['Sea of Chinnereth'] , col_gad_label, col_gad_icon) # Josh 13:27
kml.draw_node(obn.d['Succoth 1'] , col_gad_label, col_gad_icon) # Josh 13:27
kml.draw_node(obn.Zaphon, col_gad_label, col_gad_icon) # Josh 13:27

# }
# ½ Manasse {

col_manasse_ost_label = 'ff4466ff'
col_manasse_ost_icon  = 'ff4466ff'

kml.draw_node(obn.Ashtaroth            , col_manasse_ost_label, col_manasse_ost_label) # Josh 13:12
kml.draw_node(obn.Jair, col_manasse_ost_label, col_manasse_ost_icon) # Josh 13:30
# kml.draw_node(obn.Jericho, col_manasse_ost_label, col_manasse_ost_icon) # Josh 13:32
kml.draw_node(obn.Moab, col_manasse_ost_label, col_manasse_ost_icon) # Josh 13:32

# }

# }

# kml.draw_node(obn.Canaan, 'ffffffff', 'ffffffff') # Josh 14:1
# kml.draw_node(obn.d['Gilgal 1'] , 'ffffffff', 'ffffffff') # Josh 14:6
# kml.draw_node(obn.Hebron, 'ffffffff', 'ffffffff') # Josh 14:13
# kml.draw_node(obn.d['Kiriath-arba'] , 'ffffffff', 'ffffffff') # Josh 14:15
# kml.draw_node(obn.Edom, 'ffffffff', 'ffffffff') # Josh 15:1

# { Südgrenze Juda Jos 15:2 ff

kml.draw_node(obn.d['Kadesh-barnea'] , 'ffffffff', 'ffffffff') # Josh 14:6
kml.draw_node(obn.d['Zin 1'] , 'ffffffff', 'ffffffff') # Josh 15:1
kml.draw_node(obn.d['Salt Sea'] , 'ffffffff', 'ffffffff') # Josh 15:2
kml.draw_node(tqn.SalzmeerSued, 'ffffffff', 'ffffffff')
kml.draw_node(obn.Addar, 'ffffffff', 'ffffffff') # Josh 15:3
kml.draw_node(obn.Akrabbim, 'ffffffff', 'ffffffff') # Josh 15:3
kml.draw_node(tqn.Hezron, 'ffffffff', 'ffffffff') # tqn
kml.draw_node(obn.Karka, 'ffffffff', 'ffffffff') # Josh 15:3
kml.draw_node(obn.d['Zin 2'] , 'ffffffff', 'ffffffff') # Josh 15:3
kml.draw_node(obn.Azmon, 'ffffffff', 'ffffffff') # Josh 15:4
kml.draw_node(obn.d['Brook of Egypt'] , 'ffffffff', 'ffffffff') # Josh 15:4

way.Suedgrenze_Juda_Jos_15_2 = Way(tqn.SalzmeerSued, obn.Akrabbim, obn.d['Zin 2'], obn.d['Kadesh-barnea'], tqn.Hezron, obn.Addar, obn.Karka, obn.Azmon, obn.d['Brook of Egypt'], tqn.BachAegypten_Meer)
kml.draw_way(way.Suedgrenze_Juda_Jos_15_2, 'ff0000ff', 5)

# }

# kml.draw_node(obn.d['Beth-arabah'] , 'ffffffff', 'ffffffff') # Josh 15:6
# kml.draw_node(obn.d['Beth-hoglah'] , 'ffffffff', 'ffffffff') # Josh 15:6
# kml.draw_node(obn.Adummim, 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.d['Debir 2'] , 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.d['En-rogel'] , 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.d['En-shemesh'] , 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.d['Valley of Achor'] , 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.Jebusite, 'ffffffff', 'ffffffff') # Josh 15:8
# kml.draw_node(obn.Jerusalem, 'ffffffff', 'ffffffff') # Josh 15:8
# kml.draw_node(obn.d['Valley of Hinnom'] , 'ffffffff', 'ffffffff') # Josh 15:8
# kml.draw_node(obn.d['Valley of Rephaim'] , 'ffffffff', 'ffffffff') # Josh 15:8
# kml.draw_node(obn.d['Valley of the Son of Hinnom'] , 'ffffffff', 'ffffffff') # Josh 15:8
# kml.draw_node(obn.d['Baalah 2'] , 'ffffffff', 'ffffffff') # Josh 15:9
# kml.draw_node(obn.d['Kiriath-jearim'] , 'ffffffff', 'ffffffff') # Josh 15:9
# kml.draw_node(obn.d['Mount Ephron'] , 'ffffffff', 'ffffffff') # Josh 15:9
# kml.draw_node(obn.Nephtoah, 'ffffffff', 'ffffffff') # Josh 15:9
# kml.draw_node(obn.d['Beth-shemesh 1'] , 'ffffffff', 'ffffffff') # Josh 15:10
# kml.draw_node(obn.Chesalon, 'ffffffff', 'ffffffff') # Josh 15:10
# kml.draw_node(obn.d['Mount Jearim'] , 'ffffffff', 'ffffffff') # Josh 15:10
# kml.draw_node(obn.d['Mount Seir 2'] , 'ffffffff', 'ffffffff') # Josh 15:10
# kml.draw_node(obn.d['Timnah 1'] , 'ffffffff', 'ffffffff') # Josh 15:10
# kml.draw_node(obn.d['Jabneel 1'] , 'ffffffff', 'ffffffff') # Josh 15:11
# kml.draw_node(obn.d['Mount Baalah'] , 'ffffffff', 'ffffffff') # Josh 15:11
# kml.draw_node(obn.Shikkeron, 'ffffffff', 'ffffffff') # Josh 15:11
# kml.draw_node(obn.d['Great Sea'] , 'ffffffff', 'ffffffff') # Josh 15:12
# kml.draw_node(obn.d['Debir 1'] , 'ffffffff', 'ffffffff') # Josh 15:15
# kml.draw_node(obn.d['Kiriath-sepher'] , 'ffffffff', 'ffffffff') # Josh 15:15
# kml.draw_node(obn.Negeb, 'ffffffff', 'ffffffff') # Josh 15:19
# kml.draw_node(obn.d['Eder 2'] , 'ffffffff', 'ffffffff') # Josh 15:21
# kml.draw_node(obn.Jagur, 'ffffffff', 'ffffffff') # Josh 15:21
# kml.draw_node(obn.Kabzeel, 'ffffffff', 'ffffffff') # Josh 15:21
# kml.draw_node(obn.Adadah, 'ffffffff', 'ffffffff') # Josh 15:22
# kml.draw_node(obn.Dimonah, 'ffffffff', 'ffffffff') # Josh 15:22
# kml.draw_node(obn.Kinah, 'ffffffff', 'ffffffff') # Josh 15:22
# kml.draw_node(obn.d['Hazor 2'] , 'ffffffff', 'ffffffff') # Josh 15:23
# kml.draw_node(obn.Ithnan, 'ffffffff', 'ffffffff') # Josh 15:23
# kml.draw_node(obn.d['Kedesh 2'] , 'ffffffff', 'ffffffff') # Josh 15:23
# kml.draw_node(obn.Bealoth, 'ffffffff', 'ffffffff') # Josh 15:24
# kml.draw_node(obn.Telem, 'ffffffff', 'ffffffff') # Josh 15:24
# kml.draw_node(obn.d['Ziph 2'] , 'ffffffff', 'ffffffff') # Josh 15:24
# kml.draw_node(obn.d['Hazor 3'] , 'ffffffff', 'ffffffff') # Josh 15:25
# kml.draw_node(obn.d['Hazor-hadattah'] , 'ffffffff', 'ffffffff') # Josh 15:25
# kml.draw_node(obn.d['Kerioth-hezron'] , 'ffffffff', 'ffffffff') # Josh 15:25
# kml.draw_node(obn.Amam, 'ffffffff', 'ffffffff') # Josh 15:26
# kml.draw_node(obn.Moladah, 'ffffffff', 'ffffffff') # Josh 15:26
# kml.draw_node(obn.Shema, 'ffffffff', 'ffffffff') # Josh 15:26
# kml.draw_node(obn.d['Beth-pelet'] , 'ffffffff', 'ffffffff') # Josh 15:27
# kml.draw_node(obn.d['Hazar-gaddah'] , 'ffffffff', 'ffffffff') # Josh 15:27
# kml.draw_node(obn.Heshmon, 'ffffffff', 'ffffffff') # Josh 15:27
# kml.draw_node(obn.Beersheba, 'ffffffff', 'ffffffff') # Josh 15:28
# kml.draw_node(obn.Biziothiah, 'ffffffff', 'ffffffff') # Josh 15:28
# kml.draw_node(obn.d['Hazar-shual'] , 'ffffffff', 'ffffffff') # Josh 15:28
# kml.draw_node(obn.d['Baalah 1'] , 'ffffffff', 'ffffffff') # Josh 15:29
# kml.draw_node(obn.Ezem, 'ffffffff', 'ffffffff') # Josh 15:29
# kml.draw_node(obn.Iim, 'ffffffff', 'ffffffff') # Josh 15:29
# kml.draw_node(obn.Chesil, 'ffffffff', 'ffffffff') # Josh 15:30
# kml.draw_node(obn.Eltolad, 'ffffffff', 'ffffffff') # Josh 15:30
# kml.draw_node(obn.Hormah, 'ffffffff', 'ffffffff') # Josh 15:30
# kml.draw_node(obn.Madmannah, 'ffffffff', 'ffffffff') # Josh 15:31
# kml.draw_node(obn.Sansannah, 'ffffffff', 'ffffffff') # Josh 15:31
# kml.draw_node(obn.Ziklag, 'ffffffff', 'ffffffff') # Josh 15:31
# kml.draw_node(obn.d['Ain 2'] , 'ffffffff', 'ffffffff') # Josh 15:32
# kml.draw_node(obn.Lebaoth, 'ffffffff', 'ffffffff') # Josh 15:32
# kml.draw_node(obn.d['Rimmon 2'] , 'ffffffff', 'ffffffff') # Josh 15:32
# kml.draw_node(obn.Shilhim, 'ffffffff', 'ffffffff') # Josh 15:32
# kml.draw_node(obn.Ashnah, 'ffffffff', 'ffffffff') # Josh 15:33
# kml.draw_node(obn.Eshtaol, 'ffffffff', 'ffffffff') # Josh 15:33
# kml.draw_node(obn.Zorah, 'ffffffff', 'ffffffff') # Josh 15:33
# kml.draw_node(obn.Enam, 'ffffffff', 'ffffffff') # Josh 15:34
# kml.draw_node(obn.d['En-gannim 1'] , 'ffffffff', 'ffffffff') # Josh 15:34
# kml.draw_node(obn.d['Tappuah 2'] , 'ffffffff', 'ffffffff') # Josh 15:34
# kml.draw_node(obn.d['Zanoah 1'] , 'ffffffff', 'ffffffff') # Josh 15:34
# kml.draw_node(obn.Adullam, 'ffffffff', 'ffffffff') # Josh 15:35
# kml.draw_node(obn.Azekah, 'ffffffff', 'ffffffff') # Josh 15:35
# kml.draw_node(obn.d['Jarmuth 1'] , 'ffffffff', 'ffffffff') # Josh 15:35
# kml.draw_node(obn.d['Socoh 1'] , 'ffffffff', 'ffffffff') # Josh 15:35
# kml.draw_node(obn.Adithaim, 'ffffffff', 'ffffffff') # Josh 15:36
# kml.draw_node(obn.Gederah, 'ffffffff', 'ffffffff') # Josh 15:36
# kml.draw_node(obn.Gederothaim, 'ffffffff', 'ffffffff') # Josh 15:36
# kml.draw_node(obn.d['Shaaraim 1'] , 'ffffffff', 'ffffffff') # Josh 15:36
# kml.draw_node(obn.Hadashah, 'ffffffff', 'ffffffff') # Josh 15:37
# kml.draw_node(obn.d['Migdal-gad'] , 'ffffffff', 'ffffffff') # Josh 15:37
# kml.draw_node(obn.Zenan, 'ffffffff', 'ffffffff') # Josh 15:37
# kml.draw_node(obn.Dilean, 'ffffffff', 'ffffffff') # Josh 15:38
# kml.draw_node(obn.d['Joktheel 1'] , 'ffffffff', 'ffffffff') # Josh 15:38
# kml.draw_node(obn.d['Mizpeh 2'] , 'ffffffff', 'ffffffff') # Josh 15:38
# kml.draw_node(obn.Bozkath, 'ffffffff', 'ffffffff') # Josh 15:39
# kml.draw_node(obn.Eglon, 'ffffffff', 'ffffffff') # Josh 15:39
# kml.draw_node(obn.Lachish, 'ffffffff', 'ffffffff') # Josh 15:39
# kml.draw_node(obn.Cabbon, 'ffffffff', 'ffffffff') # Josh 15:40
# kml.draw_node(obn.Chitlish, 'ffffffff', 'ffffffff') # Josh 15:40
# kml.draw_node(obn.Lahmam, 'ffffffff', 'ffffffff') # Josh 15:40
# kml.draw_node(obn.d['Beth-dagon 1'] , 'ffffffff', 'ffffffff') # Josh 15:41
# kml.draw_node(obn.Gederoth, 'ffffffff', 'ffffffff') # Josh 15:41
# kml.draw_node(obn.Makkedah, 'ffffffff', 'ffffffff') # Josh 15:41
# kml.draw_node(obn.Naamah, 'ffffffff', 'ffffffff') # Josh 15:41
# kml.draw_node(obn.Ashan, 'ffffffff', 'ffffffff') # Josh 15:42
# kml.draw_node(obn.Ether, 'ffffffff', 'ffffffff') # Josh 15:42
# kml.draw_node(obn.d['Libnah 1'] , 'ffffffff', 'ffffffff') # Josh 15:42
# kml.draw_node(obn.Iphtah, 'ffffffff', 'ffffffff') # Josh 15:43
# kml.draw_node(obn.Nezib, 'ffffffff', 'ffffffff') # Josh 15:43
# kml.draw_node(obn.d['Achzib 1'] , 'ffffffff', 'ffffffff') # Josh 15:44
# kml.draw_node(obn.Keilah, 'ffffffff', 'ffffffff') # Josh 15:44
# kml.draw_node(obn.Mareshah, 'ffffffff', 'ffffffff') # Josh 15:44
# kml.draw_node(obn.Jattir, 'ffffffff', 'ffffffff') # Josh 15:48
# kml.draw_node(obn.d['Shamir 1'] , 'ffffffff', 'ffffffff') # Josh 15:48
# kml.draw_node(obn.d['Socoh 2'] , 'ffffffff', 'ffffffff') # Josh 15:48
# kml.draw_node(obn.Dannah, 'ffffffff', 'ffffffff') # Josh 15:49
# kml.draw_node(obn.d['Kiriath-sannah'] , 'ffffffff', 'ffffffff') # Josh 15:49
# kml.draw_node(obn.Anab, 'ffffffff', 'ffffffff') # Josh 15:50
# kml.draw_node(obn.Anim, 'ffffffff', 'ffffffff') # Josh 15:50
# kml.draw_node(obn.Eshtemoh, 'ffffffff', 'ffffffff') # Josh 15:50
# kml.draw_node(obn.Giloh, 'ffffffff', 'ffffffff') # Josh 15:51
# kml.draw_node(obn.d['Goshen 2'] , 'ffffffff', 'ffffffff') # Josh 15:51
# kml.draw_node(obn.d['Holon 1'] , 'ffffffff', 'ffffffff') # Josh 15:51
# kml.draw_node(obn.Arab, 'ffffffff', 'ffffffff') # Josh 15:52
# kml.draw_node(obn.d['Dumah 1'] , 'ffffffff', 'ffffffff') # Josh 15:52
# kml.draw_node(obn.Eshan, 'ffffffff', 'ffffffff') # Josh 15:52
# kml.draw_node(obn.Aphekah, 'ffffffff', 'ffffffff') # Josh 15:53
# kml.draw_node(obn.d['Beth-tappuah'] , 'ffffffff', 'ffffffff') # Josh 15:53
# kml.draw_node(obn.Janim, 'ffffffff', 'ffffffff') # Josh 15:53
# kml.draw_node(obn.Humtah, 'ffffffff', 'ffffffff') # Josh 15:54
# kml.draw_node(obn.Zior, 'ffffffff', 'ffffffff') # Josh 15:54
# kml.draw_node(obn.Carmel, 'ffffffff', 'ffffffff') # Josh 15:55
# kml.draw_node(obn.Juttah, 'ffffffff', 'ffffffff') # Josh 15:55
# kml.draw_node(obn.Maon, 'ffffffff', 'ffffffff') # Josh 15:55
# kml.draw_node(obn.d['Ziph 1'] , 'ffffffff', 'ffffffff') # Josh 15:55
# kml.draw_node(obn.Jezreel, 'ffffffff', 'ffffffff') # Josh 15:56
# kml.draw_node(obn.Jokdeam, 'ffffffff', 'ffffffff') # Josh 15:56
# kml.draw_node(obn.d['Zanoah 2'] , 'ffffffff', 'ffffffff') # Josh 15:56
# kml.draw_node(obn.d['Gibeah 2'] , 'ffffffff', 'ffffffff') # Josh 15:57
# kml.draw_node(obn.Kain, 'ffffffff', 'ffffffff') # Josh 15:57
# kml.draw_node(obn.d['Timnah 2'] , 'ffffffff', 'ffffffff') # Josh 15:57
# kml.draw_node(obn.d['Beth-zur'] , 'ffffffff', 'ffffffff') # Josh 15:58
# kml.draw_node(obn.d['Gedor 1'] , 'ffffffff', 'ffffffff') # Josh 15:58
# kml.draw_node(obn.Halhul, 'ffffffff', 'ffffffff') # Josh 15:58
# kml.draw_node(obn.d['Beth-anoth'] , 'ffffffff', 'ffffffff') # Josh 15:59
# kml.draw_node(obn.Eltekon, 'ffffffff', 'ffffffff') # Josh 15:59
# kml.draw_node(obn.Maarath, 'ffffffff', 'ffffffff') # Josh 15:59
# kml.draw_node(obn.d['Kiriath-baal'] , 'ffffffff', 'ffffffff') # Josh 15:60
# kml.draw_node(obn.Middin, 'ffffffff', 'ffffffff') # Josh 15:61
# kml.draw_node(obn.Secacah, 'ffffffff', 'ffffffff') # Josh 15:61
# kml.draw_node(obn.d['City of Salt'] , 'ffffffff', 'ffffffff') # Josh 15:62
# kml.draw_node(obn.Engedi, 'ffffffff', 'ffffffff') # Josh 15:62
# kml.draw_node(obn.Nibshan, 'ffffffff', 'ffffffff') # Josh 15:62
# kml.draw_node(obn.d['Bethel 1'] , 'ffffffff', 'ffffffff') # Josh 16:1
# kml.draw_node(obn.d['Ataroth 2'] , 'ffffffff', 'ffffffff') # Josh 16:2
# kml.draw_node(obn.d['Luz 1'] , 'ffffffff', 'ffffffff') # Josh 16:2
# kml.draw_node(obn.Gezer, 'ffffffff', 'ffffffff') # Josh 16:3
# kml.draw_node(obn.d['Lower Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 16:3
# kml.draw_node(obn.d['Ataroth-addar'] , 'ffffffff', 'ffffffff') # Josh 16:5
# kml.draw_node(obn.d['Upper Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 16:5
# kml.draw_node(obn.d['Janoah 1'] , 'ffffffff', 'ffffffff') # Josh 16:6
# kml.draw_node(obn.Michmethath, 'ffffffff', 'ffffffff') # Josh 16:6
# kml.draw_node(obn.d['Taanath-shiloh'] , 'ffffffff', 'ffffffff') # Josh 16:6
# kml.draw_node(obn.Naarah, 'ffffffff', 'ffffffff') # Josh 16:7
# kml.draw_node(obn.d['Kanah 1'] , 'ffffffff', 'ffffffff') # Josh 16:8
# kml.draw_node(obn.d['Tappuah 1'] , 'ffffffff', 'ffffffff') # Josh 16:8
# kml.draw_node(obn.d['En-tappuah'] , 'ffffffff', 'ffffffff') # Josh 17:7
# kml.draw_node(obn.Shechem, 'ffffffff', 'ffffffff') # Josh 17:7
# kml.draw_node(obn.d['Beth-shean'] , 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.Dor, 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.d['En-dor'] , 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.Ibleam, 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.Megiddo, 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.Naphath, 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.Taanach, 'ffffffff', 'ffffffff') # Josh 17:11
# kml.draw_node(obn.d['Valley of Jezreel'] , 'ffffffff', 'ffffffff') # Josh 17:16
# kml.draw_node(obn.Shiloh, 'ffffffff', 'ffffffff') # Josh 18:1
# kml.draw_node(obn.d['Beth-aven'] , 'ffffffff', 'ffffffff') # Josh 18:12
# kml.draw_node(obn.d['Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 18:14
# kml.draw_node(obn.d['Ephron 1'] , 'ffffffff', 'ffffffff') # Josh 18:15
# kml.draw_node(obn.Geliloth, 'ffffffff', 'ffffffff') # Josh 18:17
# kml.draw_node(obn.Arabah, 'ffffffff', 'ffffffff') # Josh 18:18
# kml.draw_node(obn.d['Emek-keziz'] , 'ffffffff', 'ffffffff') # Josh 18:21
# kml.draw_node(obn.Zemaraim, 'ffffffff', 'ffffffff') # Josh 18:22
# kml.draw_node(obn.Avvim, 'ffffffff', 'ffffffff') # Josh 18:23
# kml.draw_node(obn.d['Ophrah 1'] , 'ffffffff', 'ffffffff') # Josh 18:23
# kml.draw_node(obn.Parah, 'ffffffff', 'ffffffff') # Josh 18:23
# kml.draw_node(obn.d['Chephar-ammoni'] , 'ffffffff', 'ffffffff') # Josh 18:24
# kml.draw_node(obn.d['Geba 1'] , 'ffffffff', 'ffffffff') # Josh 18:24
# kml.draw_node(obn.Ophni, 'ffffffff', 'ffffffff') # Josh 18:24
# kml.draw_node(obn.Beeroth, 'ffffffff', 'ffffffff') # Josh 18:25
# kml.draw_node(obn.Gibeon, 'ffffffff', 'ffffffff') # Josh 18:25
# kml.draw_node(obn.d['Ramah 1'] , 'ffffffff', 'ffffffff') # Josh 18:25
# kml.draw_node(obn.Chephirah, 'ffffffff', 'ffffffff') # Josh 18:26
# kml.draw_node(obn.d['Mizpeh 1'] , 'ffffffff', 'ffffffff') # Josh 18:26
# kml.draw_node(obn.Mozah, 'ffffffff', 'ffffffff') # Josh 18:26
# kml.draw_node(obn.Irpeel, 'ffffffff', 'ffffffff') # Josh 18:27
# kml.draw_node(obn.Rekem, 'ffffffff', 'ffffffff') # Josh 18:27
# kml.draw_node(obn.Taralah, 'ffffffff', 'ffffffff') # Josh 18:27
# kml.draw_node(obn.d['Gibeah 1'] , 'ffffffff', 'ffffffff') # Josh 18:28
# kml.draw_node(obn.Haeleph, 'ffffffff', 'ffffffff') # Josh 18:28
# kml.draw_node(obn.Jebus, 'ffffffff', 'ffffffff') # Josh 18:28
# kml.draw_node(obn.Zela, 'ffffffff', 'ffffffff') # Josh 18:28
# kml.draw_node(obn.Sheba, 'ffffffff', 'ffffffff') # Josh 19:2
# kml.draw_node(obn.Balah, 'ffffffff', 'ffffffff') # Josh 19:3
# kml.draw_node(obn.Bethul, 'ffffffff', 'ffffffff') # Josh 19:4
# kml.draw_node(obn.d['Beth-marcaboth'] , 'ffffffff', 'ffffffff') # Josh 19:5
# kml.draw_node(obn.d['Hazar-susah'] , 'ffffffff', 'ffffffff') # Josh 19:5
# kml.draw_node(obn.d['Beth-lebaoth'] , 'ffffffff', 'ffffffff') # Josh 19:6
# kml.draw_node(obn.Sharuhen, 'ffffffff', 'ffffffff') # Josh 19:6
# kml.draw_node(obn.d['Baalath-beer'] , 'ffffffff', 'ffffffff') # Josh 19:8
# kml.draw_node(obn.Sarid, 'ffffffff', 'ffffffff') # Josh 19:10
# kml.draw_node(obn.Dabbesheth, 'ffffffff', 'ffffffff') # Josh 19:11
# kml.draw_node(obn.Jokneam, 'ffffffff', 'ffffffff') # Josh 19:11
# kml.draw_node(obn.Mareal, 'ffffffff', 'ffffffff') # Josh 19:11
# kml.draw_node(obn.d['Chisloth-tabor'] , 'ffffffff', 'ffffffff') # Josh 19:12
# kml.draw_node(obn.Daberath, 'ffffffff', 'ffffffff') # Josh 19:12
# kml.draw_node(obn.Japhia, 'ffffffff', 'ffffffff') # Josh 19:12
# kml.draw_node(obn.d['Eth-kazin'] , 'ffffffff', 'ffffffff') # Josh 19:13
# kml.draw_node(obn.d['Gath-hepher'] , 'ffffffff', 'ffffffff') # Josh 19:13
# kml.draw_node(obn.Neah, 'ffffffff', 'ffffffff') # Josh 19:13
# kml.draw_node(obn.d['Rimmon 3'] , 'ffffffff', 'ffffffff') # Josh 19:13
# kml.draw_node(obn.Hannathon, 'ffffffff', 'ffffffff') # Josh 19:14
# kml.draw_node(obn.d['Valley of Iphtahel'] , 'ffffffff', 'ffffffff') # Josh 19:14
# kml.draw_node(obn.d['Bethlehem 2'] , 'ffffffff', 'ffffffff') # Josh 19:15
# kml.draw_node(obn.Idalah, 'ffffffff', 'ffffffff') # Josh 19:15
# kml.draw_node(obn.Kattath, 'ffffffff', 'ffffffff') # Josh 19:15
# kml.draw_node(obn.Nahalal, 'ffffffff', 'ffffffff') # Josh 19:15
# kml.draw_node(obn.Shimron, 'ffffffff', 'ffffffff') # Josh 19:15
# kml.draw_node(obn.Chesulloth, 'ffffffff', 'ffffffff') # Josh 19:18
# kml.draw_node(obn.d['Jezreel 2'] , 'ffffffff', 'ffffffff') # Josh 19:18
# kml.draw_node(obn.Shunem, 'ffffffff', 'ffffffff') # Josh 19:18
# kml.draw_node(obn.Anaharath, 'ffffffff', 'ffffffff') # Josh 19:19
# kml.draw_node(obn.Hapharaim, 'ffffffff', 'ffffffff') # Josh 19:19
# kml.draw_node(obn.Shion, 'ffffffff', 'ffffffff') # Josh 19:19
# kml.draw_node(obn.Ebez, 'ffffffff', 'ffffffff') # Josh 19:20
# kml.draw_node(obn.Kishion, 'ffffffff', 'ffffffff') # Josh 19:20
# kml.draw_node(obn.Rabbith, 'ffffffff', 'ffffffff') # Josh 19:20
# kml.draw_node(obn.d['Beth-pazzez'] , 'ffffffff', 'ffffffff') # Josh 19:21
# kml.draw_node(obn.d['En-gannim 2'] , 'ffffffff', 'ffffffff') # Josh 19:21
# kml.draw_node(obn.d['En-haddah'] , 'ffffffff', 'ffffffff') # Josh 19:21
# kml.draw_node(obn.Remeth, 'ffffffff', 'ffffffff') # Josh 19:21
# kml.draw_node(obn.d['Beth-shemesh 2'] , 'ffffffff', 'ffffffff') # Josh 19:22
# kml.draw_node(obn.Shahazumah, 'ffffffff', 'ffffffff') # Josh 19:22
# kml.draw_node(obn.d['Tabor 1'] , 'ffffffff', 'ffffffff') # Josh 19:22
# kml.draw_node(obn.Achshaph, 'ffffffff', 'ffffffff') # Josh 19:25
# kml.draw_node(obn.Beten, 'ffffffff', 'ffffffff') # Josh 19:25
# kml.draw_node(obn.Hali, 'ffffffff', 'ffffffff') # Josh 19:25
# kml.draw_node(obn.Helkath, 'ffffffff', 'ffffffff') # Josh 19:25
# kml.draw_node(obn.Allammelech, 'ffffffff', 'ffffffff') # Josh 19:26
# kml.draw_node(obn.Amad, 'ffffffff', 'ffffffff') # Josh 19:26
# kml.draw_node(obn.Mishal, 'ffffffff', 'ffffffff') # Josh 19:26
# kml.draw_node(obn.d['Shihor-libnath'] , 'ffffffff', 'ffffffff') # Josh 19:26
# kml.draw_node(obn.d['Beth-dagon 2'] , 'ffffffff', 'ffffffff') # Josh 19:27
# kml.draw_node(obn.d['Beth-emek'] , 'ffffffff', 'ffffffff') # Josh 19:27
# kml.draw_node(obn.d['Cabul 1'] , 'ffffffff', 'ffffffff') # Josh 19:27
# kml.draw_node(obn.Neiel, 'ffffffff', 'ffffffff') # Josh 19:27
# kml.draw_node(obn.Ebron, 'ffffffff', 'ffffffff') # Josh 19:28
# kml.draw_node(obn.Hammon, 'ffffffff', 'ffffffff') # Josh 19:28
# kml.draw_node(obn.d['Kanah 2'] , 'ffffffff', 'ffffffff') # Josh 19:28
# kml.draw_node(obn.d['Rehob 2'] , 'ffffffff', 'ffffffff') # Josh 19:28
# kml.draw_node(obn.d['Sidon the Great'] , 'ffffffff', 'ffffffff') # Josh 19:28
# kml.draw_node(obn.d['Achzib 2'] , 'ffffffff', 'ffffffff') # Josh 19:29
# kml.draw_node(obn.Hosah, 'ffffffff', 'ffffffff') # Josh 19:29
# kml.draw_node(obn.Mahalab, 'ffffffff', 'ffffffff') # Josh 19:29
# kml.draw_node(obn.d['Ramah 2'] , 'ffffffff', 'ffffffff') # Josh 19:29
# kml.draw_node(obn.Tyre, 'ffffffff', 'ffffffff') # Josh 19:29
# kml.draw_node(obn.d['Rehob 3'] , 'ffffffff', 'ffffffff') # Josh 19:30
# kml.draw_node(obn.Ummah, 'ffffffff', 'ffffffff') # Josh 19:30
# kml.draw_node(obn.d['Adami-nekeb'] , 'ffffffff', 'ffffffff') # Josh 19:33
# kml.draw_node(obn.Heleph, 'ffffffff', 'ffffffff') # Josh 19:33
# kml.draw_node(obn.d['Jabneel 2'] , 'ffffffff', 'ffffffff') # Josh 19:33
# kml.draw_node(obn.Lakkum, 'ffffffff', 'ffffffff') # Josh 19:33
# kml.draw_node(obn.Zaanannim, 'ffffffff', 'ffffffff') # Josh 19:33
# kml.draw_node(obn.d['Aznoth-tabor'] , 'ffffffff', 'ffffffff') # Josh 19:34
# kml.draw_node(obn.Hukkok, 'ffffffff', 'ffffffff') # Josh 19:34
# kml.draw_node(obn.d['Chinnereth 2'] , 'ffffffff', 'ffffffff') # Josh 19:35
# kml.draw_node(obn.Hammath, 'ffffffff', 'ffffffff') # Josh 19:35
# kml.draw_node(obn.Rakkath, 'ffffffff', 'ffffffff') # Josh 19:35
# kml.draw_node(obn.Zer, 'ffffffff', 'ffffffff') # Josh 19:35
# kml.draw_node(obn.Ziddim, 'ffffffff', 'ffffffff') # Josh 19:35
# kml.draw_node(obn.Adamah, 'ffffffff', 'ffffffff') # Josh 19:36
# kml.draw_node(obn.d['Hazor 1'] , 'ffffffff', 'ffffffff') # Josh 19:36
# kml.draw_node(obn.d['Ramah 3'] , 'ffffffff', 'ffffffff') # Josh 19:36
# kml.draw_node(obn.d['En-hazor'] , 'ffffffff', 'ffffffff') # Josh 19:37
# kml.draw_node(obn.d['Kedesh 1'] , 'ffffffff', 'ffffffff') # Josh 19:37
# kml.draw_node(obn.d['Beth-anath'] , 'ffffffff', 'ffffffff') # Josh 19:38
# kml.draw_node(obn.d['Beth-shemesh 3'] , 'ffffffff', 'ffffffff') # Josh 19:38
# kml.draw_node(obn.Horem, 'ffffffff', 'ffffffff') # Josh 19:38
# kml.draw_node(obn.d['Migdal-el'] , 'ffffffff', 'ffffffff') # Josh 19:38
# kml.draw_node(obn.Yiron, 'ffffffff', 'ffffffff') # Josh 19:38
# kml.draw_node(obn.d['Ir-shemesh'] , 'ffffffff', 'ffffffff') # Josh 19:41
# kml.draw_node(obn.Aijalon, 'ffffffff', 'ffffffff') # Josh 19:42
# kml.draw_node(obn.Ithlah, 'ffffffff', 'ffffffff') # Josh 19:42
# kml.draw_node(obn.Shaalabbin, 'ffffffff', 'ffffffff') # Josh 19:42
# kml.draw_node(obn.Elon, 'ffffffff', 'ffffffff') # Josh 19:43
# kml.draw_node(obn.d['Baalath 1'] , 'ffffffff', 'ffffffff') # Josh 19:44
# kml.draw_node(obn.Eltekeh, 'ffffffff', 'ffffffff') # Josh 19:44
# kml.draw_node(obn.Gibbethon, 'ffffffff', 'ffffffff') # Josh 19:44
# kml.draw_node(obn.d['Bene-berak'] , 'ffffffff', 'ffffffff') # Josh 19:45
# kml.draw_node(obn.d['Gath-rimmon 1'] , 'ffffffff', 'ffffffff') # Josh 19:45
# kml.draw_node(obn.Jehud, 'ffffffff', 'ffffffff') # Josh 19:45
# kml.draw_node(obn.Joppa, 'ffffffff', 'ffffffff') # Josh 19:46
# kml.draw_node(obn.d['Me-jarkon'] , 'ffffffff', 'ffffffff') # Josh 19:46
# kml.draw_node(obn.Rakkon, 'ffffffff', 'ffffffff') # Josh 19:46
# kml.draw_node(obn.Dan, 'ffffffff', 'ffffffff') # Josh 19:47
# kml.draw_node(obn.Leshem, 'ffffffff', 'ffffffff') # Josh 19:47
# kml.draw_node(obn.d['Timnath-serah'] , 'ffffffff', 'ffffffff') # Josh 19:50


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
# kml.draw_node(obn.Edrei        , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['En-hazor'], 'ff7711ff', 'ff7711ff')

kml.draw_node(obn.Horem        , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Migdal-el'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Beth-anath'], 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.Yiron         , 'ff7711ff', 'ff7711ff')
kml.draw_node(obn.d['Beth-shemesh 3'], 'ff7711ff', 'ff7711ff')

# }

# Dan Jos 19:41 {

kml.draw_node(obn.Zorah  , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.Eshtaol, 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.d['Ir-shemesh'], 'ff55ff00', 'ff55ff00')

kml.draw_node(obn.Aijalon        , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.Ithlah         , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.Shaalabbin     , 'ff55ff00', 'ff55ff00')

kml.draw_node(obn.Ekron          , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.Elon           , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.d['Timnah 1']  , 'ff55ff00', 'ff55ff00')

kml.draw_node(obn.Eltekeh        , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.Gibbethon      , 'ff55ff00', 'ff55ff00')
kml.draw_node(obn.d['Baalath 1'] , 'ff55ff00', 'ff55ff00')

kml.draw_node(obn.Leshem         , 'ff55ff00', 'ff55ff00')

# }

kml.write('result.kml')

# Stamm_Manasse()

# write_KML_outro(kml_f)
