import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { BasicInformationApiData } from './_models';

@Injectable()
export class BasicService {
  public infos: BasicInformationApiData;

  constructor(private http: Http) { }

  getBasicInfo(): Promise<BasicInformationApiData> {
    return this.http.get('/api/basic_information')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error('Erreur durant la requête du classement');
        }
        this.infos = res.json() as BasicInformationApiData;
        return this.infos;
      });
  }

}
