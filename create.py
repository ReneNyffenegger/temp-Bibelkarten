#!/usr/bin/python3

# vim: foldmethod=marker foldmarker={,}



def Stamm_Manasse(): # {
    pass
# }

def write_KML_intro(): # {
    kml_f = open('karte_created.kml', 'w')
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
""")
    return kml_f
# }

def write_KML_outro(kml_f): # {
    kml_f.write("""
</Document>
</kml>""")
# }

kml_f = write_KML_intro()

kml_f.write("""
	<Folder>
		<name>Karte</name>
		<open>1</open>
		<Folder>
			<name>Folder</name>
			<open>1</open>
			<Placemark>
				<name>Mit Text</name>
				<description>Das ist der Text</description>
				<LookAt>
					<longitude>34.68136420025282</longitude>
					<latitude>31.92449253083083</latitude>
					<altitude>0</altitude>
					<heading>2.685299478742767</heading>
					<tilt>0</tilt>
					<range>310883.4302136681</range>
					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
				</LookAt>
				<styleUrl>#m_ylw-pushpin</styleUrl>
				<Point>
					<gx:drawOrder>1</gx:drawOrder>
					<coordinates>34.68136420025282,31.92449253083082,0</coordinates>
				</Point>
			</Placemark>
			<Placemark>
				<name>Nur Name</name>
				<LookAt>
					<longitude>34.68136430383336</longitude>
					<latitude>31.92449231718748</latitude>
					<altitude>0</altitude>
					<heading>2.685299533516287</heading>
					<tilt>0</tilt>
					<range>310883.4370406983</range>
					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
				</LookAt>
				<styleUrl>#m_ylw-pushpin</styleUrl>
				<Point>
					<gx:drawOrder>1</gx:drawOrder>
					<coordinates>34.93028888043367,31.980195320258,0</coordinates>
				</Point>
			</Placemark>
			<Placemark>
				<name>Untitled Placemark</name>
				<LookAt>
					<longitude>34.99944376518829</longitude>
					<latitude>31.74595123838236</latitude>
					<altitude>0</altitude>
					<heading>2.845835834057495</heading>
					<tilt>0</tilt>
					<range>203700.8230242897</range>
					<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
				</LookAt>
				<styleUrl>#m_ylw-pushpin</styleUrl>
				<Point>
					<gx:drawOrder>1</gx:drawOrder>
					<coordinates>34.99944376518828,31.74595123838236,0</coordinates>
				</Point>
			</Placemark>
			<Placemark>
				<name>Untitled Polygon</name>
				<styleUrl>#msn_ylw-pushpin</styleUrl>
				<Polygon>
					<tessellate>1</tessellate>
					<outerBoundaryIs>
						<LinearRing>
							<coordinates>
								35.01906060229162,31.78598741605257,0 34.97883498742767,32.01432008475683,0 34.71162012253016,31.93428660128429,0 35.01906060229162,31.78598741605257,0 
							</coordinates>
						</LinearRing>
					</outerBoundaryIs>
				</Polygon>
			</Placemark>
		</Folder>
	</Folder>

""")

write_KML_outro(kml_f)

Stamm_Manasse()

