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

  getSvgLocation(lat: number, lng: number): [number, number] {
    const svgAreas: Area[] = [
          //  [Ymin, Ymax , Xmin , Xmax ]
          [0.0117, 0.7018, 0.2877, 0.6822], //Region 0 FRANCE METROPOLITAINE
          [0.6518, 0.7712, 0.6921, 0.7235], //Region 1 CORSE
          [0.0304, 0.2172, 0.1342, 0.1864], //Region 2 SAINT-PIERRE-ET-MIQUELON
          [0.3354, 0.4218, 0.0471, 0.1557], //Region 3 SAINT MARTIN
          [0.4740, 0.5235, 0.2679, 0.2964], //Region 4.1 GUADELOUPE - MARIE-GALANTE
          [0.3227, 0.5273, 0.1764, 0.2985], //Region 4 GUADELOUPE
          [0.5273, 0.6404, 0.0729, 0.1557], //Region 5 SAINT-BARTHELEMY
          [0.7268, 0.9250, 0.0721, 0.1607], //Region 6 GUYANE
          [0.6366, 0.8564, 0.2207, 0.3236], //Region 7 MARTINIQUE
          [0.8196, 0.9365, 0.7493, 0.8450], //Region 8 WALLIS ET FUTUNA
          [0.7433, 0.8793, 0.8271, 0.9721], //Region 9 TAHITI
          [0.3888, 0.6417, 0.7400, 0.9379], //Region 10 NOUVELLE-CALEDONIE-KANAKY
          [0.1995, 0.3799, 0.8529, 0.9700], //Region 11 LA REUNION
          [0.0280, 0.3075, 0.7221, 0.8400], //Region 12 MAYOTTE
          [0.6976, 0.9848, 0.3729, 0.6264]  //Region 13 LE MONDE
      ];

    //[lat_nord, lat_sud, lng_ouest, lng_est]
    const gpsAreas: Area[] = [
          [  51.088954,   42.333188,   -4.796524,    8.203037],  //Region 0 FRANCE METROPOLITAINE
          [  43.011579,   41.367046,    8.539562,    9.559230],  //Region 1 CORSE
          [  47.144287,   46.750130,  -56.401454,  -56.126281],  //Region 2 SAINT-PIERRE-ET-MIQUELON
          [  18.124778,   18.005178,  -63.153559,  -62.970954],  //Region 3 SAINT MARTIN
          [  16.003853,   15.867515,  -61.281616,  -61.193039], //Region 4.1 GUADELOUPE - MARIE-GALANTE
          [  16.509122,   15.943341,  -61.809818,  -61.173662],  //Region 4 GUADELOUPE
          [  17.960206,   17.870865,  -62.911444,  -62.789221],  //Region 5 SAINT-BARTHELEMY
          [   5.751083,    2.109876,  -54.556803,  -51.634450],  //Region 6 GUYANNE
          [  14.879111,   14.388951,  -61.230894,  -60.810667],  //Region 7 MARTINIQUE
          [ -14.240357,  -14.361948, -178.181781, -178.000302],  //Region 8 WALLIS-ET-FUTANA
          [ -17.473598,  -17.880606, -149.915714, -149.126072],  //Region 9 TAHITI
          [ -19.540926,  -22.693430,  163.572550,  168.131190],  //Region 10 NOUVELLE-CALEDONIE-KANAKY
          [ -20.871761,  -21.387021,   55.216128,   55.835997],  //Region 11 LA REUNION
          [ -12.636997,  -12.999444,   45.018195,   45.299806],  //Region 12 MAYOTTE
          [  83.639115,  -55.496531, -168.121280,  190.384578],  //Region 13 LE MONDE
      ];

    if(lng < -168.121280){
      lng = 360 + lng
    }
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
        ((regionGps[0] - lat) / (regionGps[0] - regionGps[1]))
        * (regionSvg[1] - regionSvg[0])
      );

    // X = Xmin + ((lng - lng_ouest)/(lng_est - lng_ouest))*(Xmax-Xmin)
    const XSVG = regionSvg[2] + (
        ((lng - regionGps[2]) / (regionGps[3] - regionGps[2]))
        * (regionSvg[3] - regionSvg[2])
      );

    return([XSVG, YSVG]);
  }
}
