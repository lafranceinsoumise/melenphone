import { Injectable } from '@angular/core';

@Injectable()
export class CoordinatesConverterService {

  constructor() { }
  
  findSVGCase(AreaData, lat, lng){
    for(i = 0; i<AreaData.length; i++){
        if ((AreaData[i][0] > lat) && (AreaData[i][1] < lat) && (AreaData[i][2] < lng) && (AreaData[i][3]) > lng){
            return (i);
        }

    }
    return (AreaData.length - 1)
  }

  getSVGLocation(lat,lng){
    SVGData = [[0.001123,0.701235,0.177445,0.687332], //Region 0 FRANCE METROPOLITAINE
                    ];

    AreaData = [[51.088954,42.333188,-4.796524,8.203037], //Region 0 FRANCE METROPOLITAINE
                    ];

    region = findSVGCase(AreaData, lat, lng);

    // Calcul de la position sur le svg
    //Transformation des degres en gradiants
    AreaData[region][0] = AreaData[region][0]*3.1415/180
    AreaData[region][1] = AreaData[region][1]*3.1415/180
    lat = lat*3.1415/180

    AreaData[region][0] = Math.log(Math.tan(AreaData[region][0]) + (1/Math.cos(AreaData[region][0])))
    AreaData[region][1] = Math.log(Math.tan(AreaData[region][1]) + (1/Math.cos(AreaData[region][1])))
    lat = Math.log(Math.tan(lat) + (1/Math.cos(lat)))

    // Y = Ymin + ((lat_nord - lat)/(lat_nord - lat_sud))*(Ymax-Ymin)
    YSVG = SVGData[region][0] + (((AreaData[region][0] - lat) / (AreaData[region][0] - AreaData[region][1])) * (SVGData[region][1] - SVGData[region][0]));

    // X = Xmin + ((lng - lng_ouest)/(lng_est - lng_ouest))*(Xmax-Xmin)
    XSVG = SVGData[region][2] + (((lng - AreaData[region][2]) / (AreaData[region][3] - AreaData[region][2])) * (SVGData[region][3] - SVGData[region][2]))

    return([XSVG, YSVG]);
  }
}
