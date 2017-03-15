import { Injectable, isDevMode } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { User } from './_models';

@Injectable()
export class AuthenticationService {

    // public token: string = null;
    public currentUser: User = null;

    constructor(private http: Http) {
        // const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        // this.token = currentUser && currentUser.token;
    }

    // login(username: string, password: string) {
    //     return this.http.post('/api/token/auth', {username, password})
    //         .toPromise()
    //         .then((res: Response) => {
    //             const jsonObj = res.json();
    //             const token = jsonObj && jsonObj.token;
    //             if (token) {
    //                 this.token = token;
    //                 localStorage.setItem('currentUser', JSON.stringify({username, token}));
    //                 return true;
    //             } else {
    //                 return false;
    //             }
    //         });
    // }

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

    getExtendedInfo() {
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
        // this.token = null;
        localStorage.removeItem('currentUser');
    }

}
