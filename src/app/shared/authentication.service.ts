import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class AuthenticationService {

    public token: string;

    constructor(private http: Http) {
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    login(username: string, password: string) {
        return this.http.post('/api/token/auth', {username, password})
            .toPromise()
            .then((res: Response) => {
                const jsonObj = res.json();
                const token = jsonObj && jsonObj.token;
                if (token) {
                    this.token = token;
                    localStorage.setItem('currentUser', JSON.stringify({username, token}));
                    return true;
                } else {
                    return false;
                }
            });
    }

    getToken() {
        this.http.get('/api/token/auth')
            .toPromise()
            .then((res: Response) => {
                this.token = res.json().token;
            });
    }

    logout(): void {
        this.token = null;
        localStorage.removeItem('currentUser');
    }

}
