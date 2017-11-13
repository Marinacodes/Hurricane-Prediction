from csv import DictReader
import re

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

class HurricancePrediction:

    def read(self, data_location):
        with open(data_location, 'r') as f:
            r = DictReader(f)
            hurricanes_dict = {}
            current_id = 0
            new_hurricane = []
            for row in r:
                if current_id == row['ID']:
                    new_hurricane.append({
                        'Date': row['Date'],
                        'Time': row['Time'],
                        'Lat': row['Latitude'],
                        'Long': row['Longitude'],
                        'MaxWind': row['Maximum Wind']
                    })
                else:
                    hurricanes_dict[current_id] = new_hurricane
                    current_id = row['ID']
                    new_hurricane = [{
                        'Date': row['Date'],
                        'Time': row['Time'],
                        'Lat': row['Latitude'],
                        'Long': row['Longitude'],
                        'MaxWind': row['Maximum Wind']
                    }]

            return hurricanes_dict

    def merge_rows(self, hurricanes):
        data = []
        for key in hurricanes:
            hurricane = hurricanes[key]
            for row in range(0, len(hurricane) - 1):
                if hurricane[row + 1]:
                    data.append([int(hurricane[row]['Date']),
                        int(hurricane[row]['Time']),
                        self._lattoint(hurricane[row]['Lat']),
                        self._longtoint(hurricane[row]['Long']),
                        int(hurricane[row]['MaxWind']),
                        int(hurricane[row + 1]['Date']),
                        int(hurricane[row + 1]['Time']),
                        self._lattoint(hurricane[row + 1]['Lat']),
                        self._longtoint(hurricane[row + 1]['Long']),
                        int(hurricane[row + 1]['MaxWind'])
                    ])
        return data
		
    def extract_lats_longs(self, hurricanes):
        lats, longs = [], []
        for key in hurricanes:
            hurricane = hurricanes[key]
            for row in range(0, len(hurricane) - 1):
                if hurricane[row + 1]:
                    lats.append(self._convertlat(hurricane[row]['Lat']))
                    longs.append(self._convertlong(hurricane[row]['Long']))
        return lats, longs

    def _lattoint(self, latitude):
        if 'N' in latitude:
            return float(latitude[:-1]) + 90
        elif 'S' in latitude:
            return 90 - float(latitude[:-1])

    def _longtoint(self, longitude):
        if 'W' in longitude:
            return float(longitude[:-1]) + 180
        elif 'E' in longitude:
            return 180 - float(longitude[:-1])
			
    def _convertlat(self, latitude):
        if 'N' in latitude:
            return float(latitude[:-1])
        elif 'S' in latitude:
            return 0 - float(latitude[:-1])

    def _convertlong(self, longitude):
        if 'W' in longitude:
            return 0 - float(longitude[:-1])
        elif 'E' in longitude:
            return float(longitude[:-1])
			
def draw_map(predictor, pacific_hurricanes, atlantic_hurricanes):
    m = Basemap(projection = 'cyl', llcrnrlat = -90, urcrnrlat = 90, llcrnrlon = -180, urcrnrlon = 180, resolution='c')
 
    m.drawmapboundary()
    m.fillcontinents(color = 'gray')
 
    pac_lats, pac_longs = [], []
    atl_lats, atl_longs = [], []
	
    pac_lats, pac_longs = predictor.extract_lats_longs(pacific_hurricanes)
    atl_lats, atl_longs = predictor.extract_lats_longs(atlantic_hurricanes)
	
    a, b = m(pac_longs, pac_lats)
    c, d = m(atl_longs, atl_lats)
	
    m.plot(a, b, 'bo', markersize = 1)
    m.plot(c, d, 'ro', markersize = 1)
 
    plt.title("Hurricanes and Typhoons, 1851-2014")
    plt.show()

def main():
    predictor = HurricancePrediction()

    pacific_hurricanes = predictor.read('data/pacific.csv')
    atlantic_hurricanes = predictor.read('data/atlantic.csv')

    pacific_training = predictor.merge_rows(pacific_hurricanes)	
    atlantic_training = predictor.merge_rows(atlantic_hurricanes)
	
    draw_map(predictor, pacific_hurricanes, atlantic_hurricanes)
	
if __name__ == "__main__":
    main()
