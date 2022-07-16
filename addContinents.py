# [IMPORTANT] N'exécutez ce programme que dans le cas où votre version de la 
# table "volcans" ne contient pas la colonne "continent"!! Il sert à l'ajouter.

from geopy.geocoders import Nominatim
import pycountry_convert as pc
import sqlite3
from functools import partial

def coordinates2continent(lat,lon):
    
    geolocator = Nominatim(user_agent="geoapiExercises")
         
    
    Latitude = str(lat)
    Longitude = str(lon)
    
    reverse = partial(geolocator.reverse, language="en")
    location = reverse(Latitude+","+Longitude)
    if location == None:
        return "Antarctica"
    if location == "Türkiye":
        location = "Turkey"
    address = location.raw['address']
    
    country = address.get('country', '')
    if country == "Türkiye":
        country = "Turkey"
    

    country_alpha2 = pc.country_name_to_country_alpha2(country)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

if __name__ == '__main__':
	
    conn = sqlite3.connect('volcans.db');
    curseur = conn.cursor();
    
    #curseur.execute("ALTER TABLE volcans ADD continent TEXT;")
    
    curseur.execute("SELECT lat, lon FROM volcans;");
    
    #print(curseur.fetchall()) 
    
    list_volcans = curseur.fetchall() ;
    for i in range(len(list_volcans)):
        continent = coordinates2continent(list_volcans[i][0],list_volcans[i][1]);
        params = (continent, list_volcans[i][0], list_volcans[i][1])
        curseur.execute("UPDATE volcans SET continent = ? WHERE lat = ? AND lon = ?;", params);
    conn.commit()
    conn.close()