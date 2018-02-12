from geopy.geocoders import ArcGIS
import folium


def read_file(path):
    """(str) -> (lst)
     The function read lines from the file and return the list of them"""
    lst = []
    with open(path, "r") as f:
        for i in f:
            i = i.strip("\n")
            lst.append(i.split("\t"))
        return lst


def dictionary(lst, year):
    """"(lst)->(dict)
    The function takes a list of lines as an argument and return the
    values of dictionary according to the key,given as a second argument"""

    year = "(" + year + ")"
    d = dict()
    for i in lst:
        if year in i[0]:
            if year not in d:
                d[year] = [i[-1]]
            else:
                d[year].append(i[-1])

    return d[year]


def coordinates(lst_loc):
    """
    (list)->(list)
    The function takes the list of locations and return the list of their
    coordinates
    """
    lst = []
    geo = ArcGIS()
    for i in lst_loc:
        try:
            loc = geo.geocode(i)
            loc1 = [loc.latitude, loc.longitude]
            lst.append(loc1)
        except:
            pass
    return lst


def map():
    """Create a HTML map"""
    return folium.Map()


def point():
    """The function put points into the map and make the map coloured
     according to countries' population"""
    map1 = map()
    lst = coordinates(dictionary(read_file("locations.txt"), "1895"))
    films = folium.FeatureGroup(name='Films')
    for i in lst:
        films.add_child(folium.Marker(location=i,
                                      icon=folium.Icon()))

    population = folium.FeatureGroup(name="Population")
    population.add_child(folium.GeoJson(data=open('world.json', 'r',
                                                  encoding='utf-8-sig').read(),
                                        style_function=lambda x: {
                                            'fillColor': 'green'
                                            if x['properties'][
                                                   'POP2005'] < 10000000
                                            else 'red' if 10000000 <=
                                                          x['properties'][
                                                              'POP2005'] < 20000000
                                            else 'black'}))
    map1.add_child(population)
    map1.add_child(films)
    map1.add_child(folium.LayerControl())
    map1.save("map_lab.html")


point()
