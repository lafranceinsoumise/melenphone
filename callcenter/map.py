# -*- coding: utf-8 -*-

#Python imports
import numpy as np

def getSVGPos(lat,lng):
    #Latitude : X (augmente vers le nord)
    #Longitude : Y (augmente vers l'est)
    # Format sous tableaux : [lat_nord / Ymin, lat_sud / Ymax ,lng_ouest / Xmin ,lng_est / Xmax ]

    SVGData = [[0.001123,0.701235,0.177445,0.687332], #Region 0 FRANCE METROPOLITAINE
                    ]
    AreaData = [[51.088954,42.333188,-4.796524,8.203037], #Region 0 FRANCE METROPOLITAINE
                    ]

    region = findCaseSVG(AreaData, lat, lng) # On cherche dans quelle region on est

    #Calcul de la position sur le SVG :

    #Transformation en radians de la lat :
    AreaData[region][0] = AreaData[region][0]*np.pi/180
    AreaData[region][1] = AreaData[region][1]*np.pi/180
    lat = lat*np.pi/180

    #Projection de mercator
    AreaData[region][0] = np.log(np.tan(AreaData[region][0]) + (1/np.cos(AreaData[region][0])))
    AreaData[region][1] = np.log(np.tan(AreaData[region][1]) + (1/np.cos(AreaData[region][1])))
    lat = np.log(np.tan(lat) + (1/np.cos(lat)))

    # Y = Ymin + ((lat_nord - lat)/(lat_nord - lat_sud))*(Ymax-Ymin)
    YSVG = SVGData[region][0] + (((AreaData[region][0] - lat) / (AreaData[region][0] - AreaData[region][1])) * (SVGData[region][1] - SVGData[region][0]))

    # X = Xmin + ((lng - lng_ouest)/(lng_est - lng_ouest))*(Xmax-Xmin)
    XSVG = SVGData[region][2] + (((lng - AreaData[region][2]) / (AreaData[region][3] - AreaData[region][2])) * (SVGData[region][3] - SVGData[region][2]))

    return(XSVG, YSVG)

#Parcourt le tableau AreaData pour chercher un cas où latmin < lat < latmax et lngmin < lng < lngmax
def findCaseSVG(AreaData, lat, lng):
    for i in range (len(AreaData)):
        if ((AreaData[i][0] > lat) and (AreaData[i][1] < lat) and (AreaData[i][2] < lng) and (AreaData[i][3]) > lng):
            return (i)
    return (len(AreaData))
