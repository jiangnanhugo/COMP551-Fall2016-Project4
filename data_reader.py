import csv
import datetime
import math

import numpy as np
from nltk.cluster.kmeans import KMeansClusterer

cols =['event-id',
        'visible',
        'timestamp',
        'location-long',
        'location-lat',
        'algorithm-marked-outlier',
        'argos:altitude',
        'argos:best-level',
        'argos:calcul-freq',
        'argos:iq',
        'argos:lat1',
        'argos:lat2',
        'argos:lc',
        'argos:lon1',
        'argos:lon2',
        'argos:nb-mes',
        'argos:nb-mes-120',
        'argos:nopc',
        'argos:pass-duration',
        'argos:sensor-1',
        'argos:sensor-2',
        'argos:sensor-3',
        'argos:sensor-4',
        'argos:valid-location-manual',
        'manually-marked-outlier',
        'manually-marked-valid',
        'sensor-type',
        'individual-taxon-canonical-name',
        'tag-local-identifier',
        'individual-local-identifier',
        'study-name']

base_time = '2000-06-26 00:22:57.000'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def globe_distance(origin, destination):
    """
        Return distance in km.
        https://gist.github.com/rochacbruno/2883505

        Haversine formula example in Python
        Author: Wayne Dyck
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def parse_time(data):
    return datetime.datetime.strptime('{}000'.format(data), TIME_FORMAT)

def date_of_year(date):
    return int(date.strftime('%j'))

base_date = parse_time(base_time)

def parse_row(row):
    row[2] = parse_time(row[2]) # Parse time

    row[3] = float(row[3]) # Longitude
    row[4] = float(row[4]) # Latitude

    return (row[2], row[3], row[4], row[-2])

if __name__ == "__main__":
    data = []

    with open('data.csv', 'r') as f:
        reader = csv.reader(f, delimiter = ',')
        for index, row in enumerate(reader):
            if index == 0:
                continue
            row = parse_row(row)
            data.append(row)

    # Find max
    # maxes = {}
    # for row in data:
    #     name = row[-1]
    #     value = row[0]

    #     if name not in maxes or maxes[name][0] < value:
    #         maxes[name] = row

    # data = [row for k, row in maxes.iteritems()]

    # print data[0]

    import draw_map
    import random
    longs = [row[1] for row in data]
    lats = [row[2] for row in data]
    z = np.array([date_of_year(row[0]) for row in data])
    # z = z / float(366)

    draw_map.plot(lats, longs, z, save = False)

    # print "There are {} data points".format(len(data))
    # # data = data[:200]
    # data = np.array([(row[1], row[2]) for row in data])

    # results = []
    # for cluster_count in xrange(10, 100, 1):
    #     kclusterer = KMeansClusterer(cluster_count, distance=globe_distance, avoid_empty_clusters = True, repeats=5)
    #     assigned_clusters = kclusterer.cluster(data, assign_clusters=True)

    #     means = kclusterer.means()

    #     print "Count = {} and means are {}".format(cluster_count, means)

    #     error = sum([globe_distance(means[point], data[i]) for i, point in enumerate(assigned_clusters)])
    #     results.append((cluster_count, error))

    # with open('kmean_result.csv', 'w') as f:
    #     writer = csv.writer(f, delimiter = ',')

    #     for row in results:
    #         writer.writerow(row)