import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { LeaderboardApiData } from './_models';

@Injectable()
export class LeaderboardService {
  dailyLeaderboard: LeaderboardApiData;
  weeklyLeaderboard: LeaderboardApiData;
  monthlyLeaderboard: LeaderboardApiData;

  constructor(private http: Http) { }

  getLeaderboard(period: 'daily' | 'weekly' | 'monthly'): Promise<LeaderboardApiData> {
    return this.http.get('/api/leaderboard/daily')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error('Erreur durant la requete du classement');
        }
        return res.json().leaderboard as LeaderboardApiData;
      });
  }

  getDaily(): Promise<LeaderboardApiData> {
    return this.getLeaderboard('daily')
      .then((lb: LeaderboardApiData) => {
        return this.dailyLeaderboard = lb;
      });
  }

  getWeekly(): Promise<LeaderboardApiData> {
    return this.getLeaderboard('weekly')
      .then((lb: LeaderboardApiData) => {
        return this.weeklyLeaderboard = lb;
      });
  }

  getMonthly(): Promise<LeaderboardApiData> {
    return this.getLeaderboard('monthly')
      .then((lb: LeaderboardApiData) => {
        return this.monthlyLeaderboard = lb;
      });
  }

}
