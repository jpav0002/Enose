#!/usr/bin/python3

def get_options(header):
    dict_list = []
    for i in header:
        dict_list.append({'label': i, 'value': i})
    return dict_list

def get_location(coodinates):

    lat=coodinates['Lat']
    dirLat=coodinates['dirLat']
    lon=coodinates['Lon']
    dirLon=coodinates['dirLon']

    lat/=100
    lon/=100

    dlat,time=str(lat).split(".")
    mlat=str(time)[0:2]
    slat=str(time)[2:7]

    DDlat=int(dlat)+(int(mlat)/60)+(int(slat)/3600000)

    dlon,time=str(lon).split(".")
    mlon=str(time)[0:2]
    slon=str(time)[2:7]

    DDlon=int(dlon)+(int(mlon)/60)+(int(slon)/3600000)

    if(dirLat=="S"):
        DDlat*=-1
    if(dirLon=="W"):
        DDlon*=-1

    return DDlat,DDlon
