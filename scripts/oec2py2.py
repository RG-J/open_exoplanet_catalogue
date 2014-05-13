#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import csv
import urllib

oec_server_url = "../"
aliases = None

def get_filename(name):
    global aliases
    if aliases is None:
        global oec_server_url
        aliases_url = oec_server_url+"aliases.csv"
        try:
            aliases_csv = urllib.urlopen(aliases_url)
            aliases     = list(csv.reader(aliases_csv))
        except:
            print "Error getting Open Exoplanet Catalogue file '"+aliases_url+"'.\n"
    for alias in aliases:
        if alias[0] == name:
            return alias[1]
    
def get_system(name):
    filename = get_filename(name)
    if filename:
        system_url = oec_server_url+"systems/"+filename+".xml"
        try:
            return ET.parse(system_url).getroot()
        except:
            print "Error loading XML file '"+system_url+"'."
    
def get_planet(name):
    system = get_system(name)
    if system is not None:
        planets = system.findall(".//planet")
        for planet in planets:
            names = planet.findall(".//name")
            if name in [x.text for x in names]:
                return planet
    else:
        print "System not found."


if __name__ == "__main__":
    system = get_system("Kepler-67 b")
    print ET.tostring(system)
    print system.findtext("./distance")

    planet = get_planet("Kepler-67 b")
    print planet.find("./mass")     # not measured
    print planet.find("./radius").text
    print planet.find("./radius").attrib["errorplus"]
    print planet.find("./radius").attrib["errorminus"]

