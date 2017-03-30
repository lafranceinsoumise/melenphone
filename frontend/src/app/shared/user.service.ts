import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/toPromise';

import { AuthenticationService } from './authentication.service';
import { User, RegistrationInformations, AchievementApiData } from './_models';

@Injectable()
export class UserService {

    constructor(
        private http: Http,
        private auth: AuthenticationService) {}

    getUsers(): Promise<User[]> {
        // const headers = new Headers({ 'Authorization': 'Bearer ' + this.auth.token });
        // const options = new RequestOptions({headers});

        return this.http.get('/api/user')
            .toPromise()
            .then((res: Response) => res.json() as User[]);
    }

    getCurrentUserAchievements(): Promise<AchievementApiData> {
        return this.http.get(`/api/current_user/achievements`)
            .toPromise()
            .then((res: Response) => {
                if (res.status === 200) {
                    return res.json() as AchievementApiData;
                } else {
                    console.error('Une erreur a eu lieu lors de la récupération des trophées');
                }
            });
    }

    register(infos: RegistrationInformations) {
        // return this.http.post()
    }

}
