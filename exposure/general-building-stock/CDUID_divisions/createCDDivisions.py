#!bin/python

# Script to create census division exposure files. Written by TEHobbs on 16 Aug 2021.
# Run from CDDivisions folder

### IMPORT MODULES
import pandas as pd
import xml.etree.ElementTree as ET

#Register Namespace for this XML
ET.register_namespace('', "http://openquake.org/xmlns/nrml/0.4")
lang="{http://openquake.org/xmlns/nrml/0.4}"

### FOR EACH PROV/TERR, READ IN MAIN EXPOSURE FILE 
provs = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"] 
#ls ../oqBldgExp_??.csv | awk -F'_' '{print $2}' | awk -F'.' '{print "\""$1"\","}'

for prov in provs:
    MAIN = '../oqBldgExp_'+str(prov)
    df = pd.read_csv(str(MAIN)+'.csv')
    
    ### LIST CENSUS DIVISIONS
    regions = df['cduid'].unique()
    
    ### FOR EACH CD, GRAB THOSE ENTRIES FROM MASTER, SAVE
    for reg in regions:
        NAME = 'oqBldgExp_'+str(prov)+str(reg)
        out = df[df['cduid'] == reg]
        out.to_csv(str(NAME)+'.csv', index=False)
        
        ### MAKE XML
        tree = ET.parse(str(MAIN)+'.xml')
        root = tree.getroot()
        for elem in root.iter('assets'):
            elem.text = 'TEST'
        tree.write(str(NAME)+'.xml', encoding="UTF-8", xml_declaration=True)
        
        ### PRINT LIST
        #print(str(prov)+str(reg)+','+str(prov)) #print list of regions with province for generateSRMJobFiles.ini
        #print('"'+str(prov)+str(reg)+'"') #print list of regions for run_OQx.sh 
        #### to be copied into a txt file, and used with `awk 'ORS=" " {print $1","}' regions.txt`