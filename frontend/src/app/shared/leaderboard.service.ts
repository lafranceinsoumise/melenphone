import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { LeaderboardApiData } from './_models';

@Injectable()
export class LeaderboardService {
  leaderboards: LeaderboardApiData;

  constructor(private http: Http) { }

  getLeaderboards(): Promise<LeaderboardApiData> {
    return this.http.get('/api/leaderboard')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error('Erreur durant la requête du classement');
        }
        this.leaderboards = res.json() as LeaderboardApiData;
        return this.leaderboards;
      });
  }

}
