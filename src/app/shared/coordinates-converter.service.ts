import { Injectable } from '@angular/core';

type Area = [number, number, number, number];

@Injectable()
export class CoordinatesConverterService {
  svgData = [];

  constructor() { }

  findSvgCase(areaData: Area[], lat: number, lng: number): number {
    for (const coords of areaData) {
      if ((coords[0] > lat) && (coords[1] < lat) && (coords[2] < lng) && (coords[3]) > lng) {
          return areaData.indexOf(coords);
      }
    }
    return (areaData.length - 1);
  }

  getSvgLocation(lat, lng): [number, number] {
    const svgAreas: Area[] = [
        //Region 0 FRANCE METROPOLITAINE
        [0.001123, 0.701235, 0.177445, 0.687332], //  [Ymin, Ymax , Xmin , Xmax ]
      ];

    const gpsAreas: Area[] = [
        //Region 0 FRANCE METROPOLITAINE
        [51.088954, 42.333188, -4.796524, 8.203037], // [lat_nord, lat_sud ,lng_ouest ,lng_est]
      ];

    const regionIndex = this.findSvgCase(gpsAreas, lat, lng);
    const regionSvg = svgAreas[regionIndex];
    const regionGps = gpsAreas[regionIndex];

    // Calcul de la position sur le svg
    //Transformation des degres en gradiants
    regionGps[0] = regionGps[0] * Math.PI / 180;
    regionGps[1] = regionGps[1] * Math.PI / 180;
    lat = lat * Math.PI / 180;

    regionGps[0] = Math.log( Math.tan(regionGps[0]) + (1 / Math.cos(regionGps[0])) );
    regionGps[1] = Math.log( Math.tan(regionGps[1]) + (1 / Math.cos(regionGps[1])) );
    lat = Math.log( Math.tan(lat) + (1 / Math.cos(lat)) );

    // Y = Ymin + ((lat_nord - lat)/(lat_nord - lat_sud))*(Ymax-Ymin)
    const YSVG = regionSvg[0] + (
        ((gpsAreas[regionIndex][0] - lat) / (gpsAreas[regionIndex][0] - gpsAreas[regionIndex][1]))
        * (regionSvg[1] - regionSvg[0])
      );

    // X = Xmin + ((lng - lng_ouest)/(lng_est - lng_ouest))*(Xmax-Xmin)
    const XSVG = regionSvg[2] + (((lng - regionGps[2]) / (regionGps[3] - regionGps[2])) * (regionSvg[3] - regionSvg[2]))

    return([XSVG, YSVG]);
  }
}
