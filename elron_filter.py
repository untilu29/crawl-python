import pandas as pd
import zipfile as zf
import os, glob
from os.path import basename
import numpy as np

# Input file here
zipInput = zf.ZipFile("gtfs.zip", "r")

output_folder = 'gtfs/output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

AGENCY = output_folder + "/agency.txt"
FEED_INFO = output_folder + "/feed_info.txt"
FARE_ATT = output_folder + "/fare_attributes.txt"
FARE_RULE = output_folder + "/fare_rules.txt"
ROUTE = output_folder + "/routes.txt"
TRIP = output_folder + "/trips.txt"
CALENDAR = output_folder + "/calendar.txt"
CALENDAR_DATE = output_folder + "/calendar_dates.txt"
SHAPE = output_folder + "/shapes.txt"
STOP_TIME = output_folder + "/stop_times.txt"
STOP = output_folder + "/stops.txt"

agency = pd.read_csv(zipInput.open("agency.txt"), index_col=0)
agency_name = "ELRON"
elron_agency = agency.query('agency_name == "' + agency_name + '"')

elron_feedInfo = pd.read_csv(zipInput.open("feed_info.txt"))

fareAttributes = pd.read_csv(zipInput.open("fare_attributes.txt"))
elron_fareAttributes = fareAttributes[fareAttributes['agency_id'].isin(elron_agency.index)]

routes = pd.read_csv(zipInput.open("routes.txt"), index_col=0, dtype={'route_color': str})
elron_route = routes[routes['agency_id'].isin(elron_agency.index)]

trips = pd.read_csv(zipInput.open("trips.txt"), index_col=2, dtype={'shape_id': str})
elron_trip = trips[trips['route_id'].isin(elron_route.index)]

calendars = pd.read_csv(zipInput.open("calendar.txt"))
elron_calendar = calendars[calendars['service_id'].isin(elron_trip['service_id'])]

calendarDates = pd.read_csv(zipInput.open("calendar_dates.txt"))
elron_calendarDates = calendarDates[calendarDates['service_id'].isin(elron_calendar['service_id'])]

shapes = pd.read_csv(zipInput.open("shapes.txt"), dtype={'shape_id': str, 'shape_pt_lon': str, 'shape_pt_lat': str})
elron_shape = shapes[shapes['shape_id'].isin(elron_trip['shape_id'])]

stopTimes = pd.read_csv(zipInput.open("stop_times.txt"), dtype={'stop_id': str})
elron_stopTimes = stopTimes[stopTimes['trip_id'].isin(elron_trip.index)]

stops = pd.read_csv(zipInput.open("stops.txt"),
                    dtype={'stop_lat': float, 'stop_lon': float, 'stop_id': str, 'zone_id': str, 'alias': str,
                           'lest_x': float, 'lest_y': float})
elron_stops = stops[stops['stop_id'].isin(elron_stopTimes['stop_id'])]

fareRules = pd.read_csv(zipInput.open("fare_rules.txt"))
elron_fareRules = fareRules[
    fareRules['route_id'].isin(elron_route.index) & fareRules['origin_id'].isin(elron_stops['zone_id']) & fareRules[
        'destination_id'].isin(elron_stops['zone_id'])]

elron_stops['location_type'] = ''
elron_stops['parent_station'] = ''

elron_stops_parent_stop = elron_stops.fillna('').groupby(['stop_name'], as_index=False).agg({
    "stop_id": lambda x: '-'.join(x),
    "stop_code": lambda x: '-'.join(x),
    "zone_id": lambda x: '-'.join(x),
    "zone_name": lambda x: '-'.join(x),
    "alias": lambda x: '-'.join(x),
    "stop_area": lambda x: '-'.join(x),
    "stop_desc": lambda x: '-'.join(x),
    "stop_lat": "mean",
    "stop_lon": "mean",
    "lest_x": "mean",
    "lest_y": "mean",
    'location_type': lambda x: '1',
    'parent_station': lambda x: '',
})

for index, stop in elron_stops.iterrows():
    for idx, stop_parent in elron_stops_parent_stop.iterrows():
        if stop['stop_id'] in stop_parent['stop_id']:
            elron_stops.set_value(index, 'parent_station', stop_parent['stop_id'])

result = elron_stops.append(elron_stops_parent_stop)

elron_agency.to_csv(AGENCY, encoding='utf-8')
elron_feedInfo.to_csv(FEED_INFO, encoding='utf-8', index=False)
elron_fareAttributes.to_csv(FARE_ATT, encoding='utf-8', index=False)
elron_fareRules.to_csv(FARE_RULE, encoding='utf-8', index=False)
elron_route.to_csv(ROUTE, encoding='utf-8')
elron_trip.to_csv(TRIP, encoding='utf-8')
elron_calendar.to_csv(CALENDAR, encoding='utf-8', index=False)
elron_calendarDates.to_csv(CALENDAR_DATE, encoding='utf-8', index=False)
elron_shape.to_csv(SHAPE, encoding='utf-8', index=False)
elron_stopTimes.to_csv(STOP_TIME, encoding='utf-8', index=False)
result.to_csv(STOP, encoding='utf-8', index=False)

with zf.ZipFile(output_folder + '/estonia.zip', 'w') as myzip:
    myzip.write(AGENCY, basename(AGENCY))
    myzip.write(FEED_INFO, basename(FEED_INFO))
    myzip.write(FARE_ATT, basename(FARE_ATT))
    myzip.write(FARE_RULE, basename(FARE_RULE))
    myzip.write(ROUTE, basename(ROUTE))
    myzip.write(TRIP, basename(TRIP))
    myzip.write(CALENDAR, basename(CALENDAR))
    myzip.write(CALENDAR_DATE, basename(CALENDAR_DATE))
    myzip.write(SHAPE, basename(SHAPE))
    myzip.write(STOP_TIME, basename(STOP_TIME))
    myzip.write(STOP, basename(STOP))

for f in glob.glob(output_folder + "/*.txt"):
    os.remove(f)
