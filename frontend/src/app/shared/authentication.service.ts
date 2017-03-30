import { Injectable, isDevMode } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { User } from './_models';

@Injectable()
export class AuthenticationService {

    public currentUser: User = null;

    constructor(private http: Http) {}

    getProfile(): Promise<User> {
        return this.getBasicInfo();
    }

    getBasicInfo(): Promise<User> {
        return this.http.get('/api/current_user/profile')
            .toPromise()
            .then((res: Response) => {
                if (res.status === 401) {
                    throw new Error(`Vous n'êtes pas authentifié`);
                } else if (res.status === 404) {
                    throw new Error(`Ce profil n'existe pas`);
                } else if (res.status === 403) {
                    throw new Error(`Accès interdit. Veuillez vous connecter`);
                }
                this.currentUser = res.json() as User;
                if (isDevMode) {
                    console.group('login success');
                    console.table([this.currentUser]);
                    console.groupEnd();
                }
                return this.currentUser;
            });
    }

    getExtendedInfo(): Promise<User> {
        return this.http.get('/api/current_user/caller_information')
            .toPromise()
            .then((res: Response) => {
                if (res.status === 200) {
                    return res.json();
                } else {
                    return {};
                }
            });
    }

    logout(): void {
        localStorage.removeItem('currentUser');
    }

}
