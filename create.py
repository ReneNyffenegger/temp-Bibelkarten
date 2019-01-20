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
             kml_f.write('<description>{:s}</description><styleUrl>#note</styleUrl>'.format(node['node'].description))

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
      <Folder>
	<name>Untitled Folder</name>
	<Camera>
		<longitude>35.08266913626239</longitude>
		<latitude>32.46765784186947</latitude>
		<altitude>558490.9801019359</altitude>
		<heading>4.538740631097303</heading>
		<tilt>1.175330159089605</tilt>
		<roll>-2.27684395179298</roll>
		<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
	</Camera>
""") # }
          return kml_f
     # }

      def write_outro(self, kml_f): # {
          kml_f.write("""
      </Folder>
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

#                                               East              North
addTQ84Node('SalzmeerSued'                    , 35, 23,  4.67,    30, 55, 41.19)
addTQ84Node('Hezron'                          , 34, 40, 55.94,    30, 53, 49.65)
addTQ84Node('BachAegypten_Meer'               , 33, 49, 44.55,    31,  9, 14.32)
addTQ84Node('SalzmeerJordan'                  , 35, 33, 29.49,    31, 45, 43.21)
addTQ84Node('SteinBohans'                     , 35, 24, 36.99,    31, 49, 54.48)
addTQ84Node('GilgalgegenueberAdummim'         , 35, 20, 44.50,    31, 49, 41.98)
addTQ84Node('Geliloth'                        , 35, 20, 10.54,    31, 49, 18.81) # openbible seems to be too far in the east!
addTQ84Node('Berg_Suedlich_unterem_Beth_Horon', 35,  7, 45.86,    31, 52, 13.40) # Jos 18:13
addTQ84Node('Scheba'                          , 34, 50,  6.55,    31, 11, 40.41) # Jos 19:2
addTQ84Node('Bethul'                          , 34, 42, 48.44,    31, 18, 46.66) # Jos 19:4
# addTQ84Node('Scheba'                          , 34, 50, 34.39,    31, 13, 13.11) # Jos 19

tqn.GilgalgegenueberAdummim.description = "Gegenüber der Anhöhe Adummim, südlich vom Bach (Jos 15:7)"


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
obn.Mearah.description    = "Gehört den Zidoniern (Jos 13:4)"
obn.d['Aphek 1'].description  = "Grenze der Amoriter? (Jos 13:4), vgl Aphek 3"
obn.d['Aphek 3'].description  = "Grenze der Amoriter? (Jos 13:4), vgl Aphek 1"
obn.d['Baal-gad'].description  = "Am Fuß des Berges Hermon (Jos 13:5)"
obn.d['Aroer 1'].description  = "Am Ufer des Flusses Arnon (Jos 13:16)"
obn.d['Aroer 2'].description  = "Liegt vor Rabba (Jos 13:25)"

obn.d['Dibon 1'].description  = "In der Ebene (Jos 13:17 ff)"
obn.d['Bamoth-baal'].description  = "In der Ebene (Jos 13:17 ff)"
obn.d['Beth-baal-meon'].description  = "In der Ebene (Jos 13:17 ff)"
obn.Jahaz.description                = "In der Ebene (Jos 13:17 ff)"
obn.Kedemoth.description             = "In der Ebene (Jos 13:17 ff)"
obn.Mephaath.description             = "In der Ebene (Jos 13:17 ff)"
obn.d['Kiriathaim 1'].description    = "In der Ebene (Jos 13:17 ff)"
obn.Sibmah.description               = "In der Ebene (Jos 13:17 ff)"
obn.d['Zereth-shahar'].description   = "Auf dem Berg der Talebene (Jos 13:19)"
obn.d['Baalah 2'].description        = "Baala ist Kirjath-Jearim (Jos 15:9)"
obn.d['Kiriath-jearim'].description  = "Baala ist Kirjath-Jearim (Jos 15:9)<br/>Kirjath-Baal ist Kirjath-Jearim (Jos 15:60/Jos 18:14)<br/>Eine Stadt der Kinder Juda (Jos 18:14)"
obn.d['Kiriath-baal'  ].description  = "Kirjath-Jearim ist Kirjath-Baal (Jos 15:60/Jos 18:14)<br/>Eine Stadt der Kinder Juda (Jos 18:14)"
obn.d['Mount Jearim'].description    = "Nordseite ist Kesalon (Jos 15:10)"
obn.Kesalon                          = "Nordseite des Berges Jearim ist Kesalon (Jos 15:10)"
obn.d['Kerioth-hezron'].description  = "Kerijoth-Hezron ist Hazor (Jos 15:25)"
obn.d['Hazor 3'].description         = "Kerijoth-Hezron ist Hazor (Jos 15:25)"
obn.Beersheba.description            = "Eine Stadt Simeons (Jos 19:2)"
obn.Moladah.description            = "Eine Stadt Simeons (Jos 19:3)"

obn.Rabbah.description = "Nahe bei Aroer 2 (Jos 13:25)"
obn.Hebron.description = "Die Stadt Arbas, des Vaters Enaks, inmitten Juda (Jos 15:13)"
obn.d['Debir 1'].description = "Der Name von Debir war Kirjath-Sepher (Jos 15:15)"

obn.d['Ataroth 2'].description = "Grenze der Arkiter (Jos 16:2)"
obn.d['Lower Beth-horon'].description = "Grenze der Japhletiter (Jos 16:3)"

obn.d['Beth-aven'].description = 'Bei/in der Wüste (Jos 18:12)'
obn.d['Bethel 1'].description = 'Lus = Bethel (Jos 18:13)'
obn.d['Luz 1'].description = 'Lus = Bethel (Jos 18:13)'

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
kml.draw_node(obn.d['Aphek 2'] , 'ffffffff', 'ffffffff')
kml.draw_node(obn.d['Aphek 3'] , 'ffffffff', 'ffffffff')

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
kml.draw_node(obn.Moab, col_manasse_ost_label, col_manasse_ost_icon) # Josh 13:32

# }

# }

# { Jos 15 - Juda

# kml.draw_node(obn.Canaan, 'ffffffff', 'ffffffff') # Josh 14:1
kml.draw_node(obn.Hebron, 'ffffffff', 'ffffffff') # Josh 14:13


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

kml.draw_node(tqn.SalzmeerJordan, 'ffffffff', 'ffffffff')
kml.draw_node(tqn.SteinBohans      , 'ffffffff', 'ffffffff') # Josh 15:6
kml.draw_node(obn.d['Debir 2'] , 'ffffffff', 'ffffffff') # Josh 15:7
kml.draw_node(obn.d['Gilgal 1'] , 'ffffffff', 'ffffffff') # Josh 14:6
# kml.draw_node(obn.Adummim, 'ffffffff', 'ffffffff') # Josh 15:7
kml.draw_node(tqn.GilgalgegenueberAdummim, 'ffffffff', 'ffffffff')
kml.draw_node(obn.d['En-shemesh'] , 'ffffffff', 'ffffffff') # Josh 15:7
kml.draw_node(obn.d['En-rogel'] , 'ffffffff', 'ffffffff') # Josh 15:7
kml.draw_node(obn.d['Valley of Hinnom'] , 'ffffffff', 'ffffffff') # Josh 15:8



# kml.draw_node(obn.d['Valley of Achor'] , 'ffffffff', 'ffffffff') # Josh 15:7
# kml.draw_node(obn.Jebusite, 'ffffffff', 'ffffffff') # Josh 15:8
kml.draw_node(obn.d['Valley of the Son of Hinnom'] , 'ffffffff', 'ffffffff') # Josh 15:8
kml.draw_node(obn.d['Valley of Rephaim'] , 'ffffffff', 'ffffffff') # Josh 15:8
kml.draw_node(obn.Nephtoah, 'ffffffff', 'ffffffff') # Josh 15:9
kml.draw_node(obn.d['Mount Ephron'] , 'ffffffff', 'ffffffff') # Josh 15:9
kml.draw_node(obn.d['Baalah 2'] , 'ffffffff', 'ffffffff') # Josh 15:9
kml.draw_node(obn.d['Mount Seir 2'] , 'ffffffff', 'ffffffff') # Josh 15:10
kml.draw_node(obn.d['Mount Jearim'] , 'ffffffff', 'ffffffff') # Josh 15:10
kml.draw_node(obn.Chesalon, 'ffffffff', 'ffffffff') # Josh 15:10
kml.draw_node(obn.d['Beth-shemesh 1'] , 'ffffffff', 'ffffffff') # Josh 15:10
kml.draw_node(obn.d['Timnah 1'] , 'ffffffff', 'ffffffff') # Josh 15:10
kml.draw_node(obn.Shikkeron, 'ffffffff', 'ffffffff') # Josh 15:11
kml.draw_node(obn.d['Mount Baalah'] , 'ffffffff', 'ffffffff') # Josh 15:11
kml.draw_node(obn.d['Jabneel 1'] , 'ffffffff', 'ffffffff') # Josh 15:11

way.Nordgrenze_Juda_Jos_15_5 = Way( 
       tqn.SalzmeerJordan,
       obn.d['Beth-hoglah'] ,
       obn.d['Beth-arabah'] ,
       tqn.SteinBohans,
       obn.d['Debir 2'] ,
#      obn.d['Gilgal 1'] ,
       obn.Adummim,
       obn.d['En-shemesh'] ,
       obn.d['En-rogel'] ,
       obn.d['Valley of Hinnom'],
       obn.d['Valley of the Son of Hinnom'] ,
       obn.d['Valley of Rephaim'] ,
       obn.Nephtoah,
       obn.d['Mount Ephron'] ,
       obn.d['Kiriath-jearim'] ,
       obn.d['Baalah 2'] ,
       obn.d['Mount Seir 2'] ,
       obn.d['Mount Jearim'] ,
       obn.Chesalon,
       obn.d['Beth-shemesh 1'] ,
       obn.d['Timnah 1'] ,
       obn.Shikkeron,
       obn.d['Mount Baalah'] ,
       obn.d['Jabneel 1'] )
kml.draw_way(way.Nordgrenze_Juda_Jos_15_5, 'ff0000ff', 5)



kml.draw_node(obn.d['Valley of Achor'] , 'ffffffff', 'ffffffff') # Josh 15:7

# }
# kml.draw_node(obn.d['Great Sea'] , 'ffffffff', 'ffffffff') # Josh 15:12
kml.draw_node(obn.d['Debir 1'] , 'ffffffff', 'ffffffff') # Josh 15:15
# kml.draw_node(obn.d['Kiriath-sepher'] , 'ffffffff', 'ffffffff') # Josh 15:15
kml.draw_node(obn.Negeb, 'ffffffff', 'ffffffff') # Josh 15:19

# { Judas Städte im Süden Jos 15:21-32

color_label_juda_sueden = 'ff3355ff'
color_icon_juda_sueden  = 'ff3355ff'

kml.draw_node(obn.Jagur                 , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:21
kml.draw_node(obn.Kabzeel               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:21
kml.draw_node(obn.d['Eder 2']           , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:21

kml.draw_node(obn.Adadah                , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:22
kml.draw_node(obn.Dimonah               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:22
kml.draw_node(obn.Kinah                 , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:22

kml.draw_node(obn.d['Hazor 2']          , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:23
kml.draw_node(obn.Ithnan                , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:23
kml.draw_node(obn.d['Kedesh 2']         , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:23
kml.draw_node(obn.Bealoth               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:24
kml.draw_node(obn.Telem                 , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:24
kml.draw_node(obn.d['Ziph 2']           , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:24
kml.draw_node(obn.d['Hazor 3']          , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:25
kml.draw_node(obn.d['Hazor-hadattah']   , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:25
kml.draw_node(obn.d['Kerioth-hezron']   , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:25
kml.draw_node(obn.Amam                  , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:26
kml.draw_node(obn.Moladah               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:26
kml.draw_node(obn.Shema                 , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:26
kml.draw_node(obn.d['Beth-pelet']       , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:27
kml.draw_node(obn.d['Hazar-gaddah']     , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:27
kml.draw_node(obn.Heshmon               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:27
kml.draw_node(obn.Beersheba             , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:28
kml.draw_node(obn.Biziothiah            , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:28
kml.draw_node(obn.d['Hazar-shual']      , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:28
kml.draw_node(obn.d['Baalah 1']         , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:29
kml.draw_node(obn.Ezem                  , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:29
kml.draw_node(obn.Iim                   , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:29
kml.draw_node(obn.Chesil                , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:30
kml.draw_node(obn.Eltolad               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:30
kml.draw_node(obn.Hormah                , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:30
kml.draw_node(obn.Madmannah             , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:31
kml.draw_node(obn.Sansannah             , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:31
kml.draw_node(obn.Ziklag                , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:31
kml.draw_node(obn.d['Ain 2']            , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:32
kml.draw_node(obn.Lebaoth               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:32
kml.draw_node(obn.d['Rimmon 2']         , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:32
kml.draw_node(obn.Shilhim               , color_label_juda_sueden, color_icon_juda_sueden) # Josh 15:32

# }

# Judas Städte in der Niederung Jos 15:33-47 {

color_label_juda_niederung = 'ff5533ff'
color_icon_juda_niederung  = 'ff5533ff'

kml.draw_node(obn.Ashnah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:33
kml.draw_node(obn.Eshtaol, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:33
kml.draw_node(obn.Zorah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:33
kml.draw_node(obn.Enam, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:34
kml.draw_node(obn.d['En-gannim 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:34
kml.draw_node(obn.d['Tappuah 2'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:34
kml.draw_node(obn.d['Zanoah 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:34
kml.draw_node(obn.Adullam, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:35
kml.draw_node(obn.Azekah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:35
kml.draw_node(obn.d['Jarmuth 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:35
kml.draw_node(obn.d['Socoh 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:35
kml.draw_node(obn.Adithaim, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:36
kml.draw_node(obn.Gederah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:36 kml.draw_node(obn.Gederothaim, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:36
kml.draw_node(obn.d['Shaaraim 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:36
kml.draw_node(obn.Hadashah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:37
kml.draw_node(obn.d['Migdal-gad'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:37
kml.draw_node(obn.Zenan, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:37
kml.draw_node(obn.Dilean, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:38
kml.draw_node(obn.d['Joktheel 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:38
kml.draw_node(obn.d['Mizpeh 2'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:38
kml.draw_node(obn.Bozkath, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:39
kml.draw_node(obn.Eglon, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:39
kml.draw_node(obn.Lachish, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:39
kml.draw_node(obn.Cabbon, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:40
kml.draw_node(obn.Chitlish, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:40
kml.draw_node(obn.Lahmam, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:40
kml.draw_node(obn.d['Beth-dagon 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:41
kml.draw_node(obn.Gederoth, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:41
kml.draw_node(obn.Makkedah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:41
kml.draw_node(obn.Naamah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:41
kml.draw_node(obn.Ashan, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:42
kml.draw_node(obn.Ether, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:42
kml.draw_node(obn.d['Libnah 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:42
kml.draw_node(obn.Iphtah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:43
kml.draw_node(obn.Nezib, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:43
kml.draw_node(obn.d['Achzib 1'] , color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:44
kml.draw_node(obn.Keilah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:44
kml.draw_node(obn.Mareshah, color_label_juda_niederung, color_icon_juda_niederung) # Josh 15:44

# }

# { Judas Städte im Gebirge Jos 15:48-60

color_label_juda_gebirge = 'ff1199cc'
color_icon_juda_gebirge  = 'ff1199cc'

kml.draw_node(obn.Jattir, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:48
kml.draw_node(obn.d['Shamir 1'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:48
kml.draw_node(obn.d['Socoh 2'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:48
kml.draw_node(obn.Dannah, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:49
kml.draw_node(obn.d['Kiriath-sannah'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:49
kml.draw_node(obn.Anab, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:50
kml.draw_node(obn.Anim, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:50
kml.draw_node(obn.Eshtemoh, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:50
kml.draw_node(obn.Giloh, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:51
kml.draw_node(obn.d['Goshen 2'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:51
kml.draw_node(obn.d['Holon 1'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:51
kml.draw_node(obn.Arab, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:52
kml.draw_node(obn.d['Dumah 1'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:52
kml.draw_node(obn.Eshan, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:52
kml.draw_node(obn.Aphekah, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:53
kml.draw_node(obn.d['Beth-tappuah'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:53
kml.draw_node(obn.Janim, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:53
kml.draw_node(obn.Humtah, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:54
kml.draw_node(obn.Zior, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:54
kml.draw_node(obn.Carmel, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:55
kml.draw_node(obn.Juttah, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:55
kml.draw_node(obn.Maon, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:55
kml.draw_node(obn.d['Ziph 1'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:55
kml.draw_node(obn.Jezreel, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:56
kml.draw_node(obn.Jokdeam, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:56
kml.draw_node(obn.d['Zanoah 2'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:56
kml.draw_node(obn.d['Gibeah 2'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:57
kml.draw_node(obn.Kain, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:57
kml.draw_node(obn.d['Timnah 2'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:57
kml.draw_node(obn.d['Beth-zur'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:58
kml.draw_node(obn.d['Gedor 1'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:58
kml.draw_node(obn.Halhul, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:58
kml.draw_node(obn.d['Beth-anoth'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:59
kml.draw_node(obn.Eltekon, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:59
kml.draw_node(obn.Maarath, color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:59
kml.draw_node(obn.d['Kiriath-baal'] , color_label_juda_gebirge, color_icon_juda_gebirge) # Josh 15:60

# }

# { Judas Städte in der Wüste

color_label_juda_wueste = 'ff9911cc'
color_icon_juda_wueste  = 'ff9911cc'

kml.draw_node(obn.Middin, color_label_juda_wueste, color_icon_juda_wueste) # Josh 15:61
kml.draw_node(obn.Secacah, color_label_juda_wueste, color_icon_juda_wueste) # Josh 15:61
kml.draw_node(obn.d['City of Salt'] , color_label_juda_wueste, color_icon_juda_wueste) # Josh 15:62
kml.draw_node(obn.Engedi, color_label_juda_wueste, color_icon_juda_wueste) # Josh 15:62
kml.draw_node(obn.Nibshan, color_label_juda_wueste, color_icon_juda_wueste) # Josh 15:62

# }

# }

# { Jos 16  

  # { Joseph

kml.draw_node(obn.d['Luz 1'] , 'ffffffff', 'ffffffff') # Josh 16:2
kml.draw_node(obn.d['Ataroth 2'] , 'ffffffff', 'ffffffff') # Josh 16:2

kml.draw_node(obn.d['Lower Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 16:3
kml.draw_node(obn.Gezer, 'ffffffff', 'ffffffff') # Josh 16:3

way.Suedgrenze_Joseph_16_2 = Way(obn.Jericho, obn.d['Bethel 1'], obn.d['Luz 1'], obn.d['Ataroth 2'], obn.d['Lower Beth-horon'], obn.Gezer)
kml.draw_way(way.Suedgrenze_Joseph_16_2, 'ff336699', 5)

  # { Ostgrenze Ephraim

kml.draw_node(obn.d['Ataroth-addar'] , 'ffffffff', 'ffffffff') # Josh 16:5
# kml.draw_node(obn.d['Ataroth 2'] , 'ffffffff', 'ffffffff') #
kml.draw_node(obn.d['Upper Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 16:5
kml.draw_node(obn.Michmethath, 'ffffffff', 'ffffffff') # Josh 16:6
kml.draw_node(obn.d['Taanath-shiloh'] , 'ffffffff', 'ffffffff') # Josh 16:6
kml.draw_node(obn.d['Janoah 2'] , 'ffffffff', 'ffffffff') # Josh 16:6
kml.draw_node(obn.Naarah, 'ffffffff', 'ffffffff') # Josh 16:7

way.Ostgrenze_Ephraim_Jos_16_5 = Way(obn.d['Ataroth-addar'], obn.d['Upper Beth-horon'], obn.Michmethath, obn.d['Taanath-shiloh'], obn.d['Janoah 2'], obn.d['Ataroth 2'], obn.Naarah, obn.Jericho) 
kml.draw_way(way.Ostgrenze_Ephraim_Jos_16_5, 'ff663399', 5)


kml.draw_node(obn.d['Kanah 1'] , 'ffffffff', 'ffffffff') # Josh 16:8
kml.draw_node(obn.d['Tappuah 1'] , 'ffffffff', 'ffffffff') # Josh 16:8
way.Westgrenze_Ephraim_Jos_16_8 = Way(obn.d['Kanah 1'], obn.d['Tappuah 1'])
kml.draw_way(way.Westgrenze_Ephraim_Jos_16_8, 'ff663399', 5)

  # }

  # }


# } 
# { Jos 17 
kml.draw_node(obn.Shechem, 'ffffffff', 'ffffffff') # Josh 17:7
kml.draw_node(obn.d['En-tappuah'] , 'ffffffff', 'ffffffff') # Josh 17:7

way.Grenze_Manasse_Josh_17_7 = Way(obn.Michmethath, obn.d['En-tappuah'], obn.d['Kanah 1'])
kml.draw_way(way.Grenze_Manasse_Josh_17_7, 'ffff6666', 5)

color_label_manasse_in_issaschar_asser = 'ffaa9966'
color_icon_manasse_in_issaschar_asser = 'ffaa9966'

kml.draw_node(obn.d['Beth-shean'] , color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.Ibleam, color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.Dor, color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.d['En-dor'] , color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.Taanach, color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.Megiddo, color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
# kml.draw_node(obn.Naphath, color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:11
kml.draw_node(obn.d['Valley of Jezreel'] , color_label_manasse_in_issaschar_asser, color_icon_manasse_in_issaschar_asser) # Josh 17:16

# }
# { Jos 18
kml.draw_node(obn.Shiloh, 'ffffffff', 'ffffffff') # Josh 18:1

way.Grenze_Benjamin_West_Jos_18_11 = Way(obn.Jericho, obn.d['Beth-aven'], obn.d['Luz 1'], obn.d['Ataroth-addar'], obn.d['Kiriath-baal'])
way.Grenze_Benjamin_Sued_Joas_18_15 = Way(obn.d['Kiriath-jearim'], obn.Nephtoah, obn.d['Valley of the Son of Hinnom'], obn.d['Valley of Hinnom'], obn.d['En-rogel'], obn.d['En-shemesh'], tqn.Geliloth, tqn.SteinBohans, obn.d['Beth-hoglah'])
kml.draw_way(way.Grenze_Benjamin_West_Jos_18_11, 'ff558822', 5)
kml.draw_way(way.Grenze_Benjamin_Sued_Joas_18_15, 'ff558822', 5)





kml.draw_node(obn.d['Beth-aven'] , 'ffffffff', 'ffffffff') # Josh 18:12
kml.draw_node(obn.d['Beth-horon'] , 'ffffffff', 'ffffffff') # Josh 18:14
kml.draw_node(obn.d['Ephron 1'] , 'ffffffff', 'ffffffff') # Josh 18:15
kml.draw_node(obn.Geliloth, 'ffffffff', 'ffffffff') # Josh 18:17
kml.draw_node(obn.Arabah, 'ffffffff', 'ffffffff') # Josh 18:18
kml.draw_node(obn.d['Geba 1'] , 'ffffffff', 'ffffffff') # Josh 18:24
kml.draw_node(obn.Ophni, 'ffffffff', 'ffffffff') # Josh 18:24
kml.draw_node(obn.Beeroth, 'ffffffff', 'ffffffff') # Josh 18:25
kml.draw_node(obn.Gibeon, 'ffffffff', 'ffffffff') # Josh 18:25
kml.draw_node(obn.d['Ramah 1'] , 'ffffffff', 'ffffffff') # Josh 18:25
kml.draw_node(obn.d['Mizpeh 1'] , 'ffffffff', 'ffffffff') # Josh 18:26

kml.draw_node(tqn.Berg_Suedlich_unterem_Beth_Horon, 'ffffffff', 'ffffffff') # Josua 18:13

kml.draw_node(obn.Jebus, 'ffffffff', 'ffffffff') # Josh 18:28

# { Städte von Benjamin Jos 18:21 ff

color_label_benjamin = 'ff558822'
color_icon_benjamin = 'ff558822'

kml.draw_node(obn.Jericho, color_label_benjamin, color_icon_benjamin)
kml.draw_node(obn.d['Beth-hoglah'] , color_label_benjamin, color_icon_benjamin) # Josh 15:6
kml.draw_node(obn.d['Emek-keziz'] , color_label_benjamin, color_icon_benjamin) # Josh 18:21
kml.draw_node(obn.d['Beth-arabah'] , color_label_benjamin, color_icon_benjamin) # Josh 15:6
kml.draw_node(obn.Zemaraim, color_label_benjamin, color_icon_benjamin) # Josh 18:22
kml.draw_node(obn.d['Bethel 1'] , color_label_benjamin, color_icon_benjamin) # Josh 16:1
kml.draw_node(obn.Avvim, color_label_benjamin, color_icon_benjamin) # Josh 18:23
kml.draw_node(obn.Parah, color_label_benjamin, color_icon_benjamin) # Josh 18:23
kml.draw_node(obn.d['Ophrah 1'] , color_label_benjamin, color_icon_benjamin) # Josh 18:23
kml.draw_node(obn.d['Chephar-ammoni'] , color_label_benjamin, color_icon_benjamin) # Josh 18:24
kml.draw_node(obn.Chephirah, color_label_benjamin, color_icon_benjamin) # Josh 18:26
kml.draw_node(obn.Mozah, color_label_benjamin, color_icon_benjamin) # Josh 18:26
kml.draw_node(obn.Rekem, color_label_benjamin, color_icon_benjamin) # Josh 18:27
kml.draw_node(obn.Irpeel, color_label_benjamin, color_icon_benjamin) # Josh 18:27
kml.draw_node(obn.Taralah, color_label_benjamin, color_icon_benjamin) # Josh 18:27
kml.draw_node(obn.Zela, color_label_benjamin, color_icon_benjamin) # Josh 18:28
kml.draw_node(obn.Haeleph, color_label_benjamin, color_icon_benjamin) # Josh 18:28
kml.draw_node(obn.Jerusalem, color_label_benjamin, color_icon_benjamin) # Josh 15:8
kml.draw_node(obn.d['Gibeah 1'] , color_label_benjamin, color_icon_benjamin) # Josh 18:28
kml.draw_node(obn.d['Kiriath-jearim'] , color_label_benjamin, color_icon_benjamin) # Josh 15:9

# }

# }

# { Jos 19

# { Simeon Jos 19:1-9

color_label_simeon = 'ffcc5522'
color_icon_simeon = 'ffcc5522'

#  kml.draw_node(obn.Sheba, color_label_simeon, color_icon_simeon) # Josh 19:2   confused with Sheba
kml.draw_node(tqn.Scheba, color_label_simeon, color_icon_simeon)


kml.draw_node(obn.Balah, color_label_simeon, color_icon_simeon) # Josh 19:3

# kml.draw_node(obn.Bethul, color_label_simeon, color_icon_simeon) # Josh 19:4
kml.draw_node(tqn.Bethul, color_label_simeon, color_icon_simeon) # Jos 19:4

kml.draw_node(obn.d['Beth-marcaboth'] , color_label_simeon, color_icon_simeon) # Josh 19:5
kml.draw_node(obn.d['Hazar-susah'] , color_label_simeon, color_icon_simeon) # Josh 19:5
kml.draw_node(obn.d['Beth-lebaoth'] , color_label_simeon, color_icon_simeon) # Josh 19:6
kml.draw_node(obn.Sharuhen, color_label_simeon, color_icon_simeon) # Josh 19:6
kml.draw_node(obn.d['Baalath-beer'] , color_label_simeon, color_icon_simeon) # Josh 19:8

# }

kml.draw_node(obn.Sarid, 'ffffffff', 'ffffffff') # Josh 19:10
kml.draw_node(obn.Mareal, 'ffffffff', 'ffffffff') # Josh 19:11
kml.draw_node(obn.Dabbesheth, 'ffffffff', 'ffffffff') # Josh 19:11
kml.draw_node(obn.Jokneam, 'ffffffff', 'ffffffff') # Josh 19:11
kml.draw_node(obn.d['Chisloth-tabor'] , 'ffffffff', 'ffffffff') # Josh 19:12
kml.draw_node(obn.Daberath, 'ffffffff', 'ffffffff') # Josh 19:12
kml.draw_node(obn.Japhia, 'ffffffff', 'ffffffff') # Josh 19:12
kml.draw_node(obn.d['Gath-hepher'] , 'ffffffff', 'ffffffff') # Josh 19:13
kml.draw_node(obn.d['Eth-kazin'] , 'ffffffff', 'ffffffff') # Josh 19:13
kml.draw_node(obn.d['Rimmon 3'] , 'ffffffff', 'ffffffff') # Josh 19:13
kml.draw_node(obn.Neah, 'ffffffff', 'ffffffff') # Josh 19:13
kml.draw_node(obn.Hannathon, 'ffffffff', 'ffffffff') # Josh 19:14
kml.draw_node(obn.d['Valley of Iphtahel'] , 'ffffffff', 'ffffffff') # Josh 19:14

way.Grenze_Sebulon_Jos_19_11 = Way(
  obn.Sarid,
  obn.Mareal,
  obn.Dabbesheth,
  obn.Jokneam,
  obn.d['Chisloth-tabor'] ,
  obn.Daberath,
  obn.Japhia,
  obn.d['Gath-hepher'] ,
  obn.d['Eth-kazin'] ,
  obn.d['Rimmon 3'] ,
  obn.Neah,
  obn.Hannathon,
  obn.d['Valley of Iphtahel'])
kml.draw_way(way.Grenze_Sebulon_Jos_19_11, 'ff775588', 5)

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
kml.draw_node(obn.Sidon, 'ffffffff', 'ffffffff') # Josh 19:28
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

# }

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


kml.draw_node(obn.Patmos, 'ffffffff', 'ffffffff')
kml.draw_node(obn.Elam  , 'ffffffff', 'ffffffff')

kml.write('result.kml')

# Stamm_Manasse()

# write_KML_outro(kml_f)
