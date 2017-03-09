import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/toPromise';

import { AuthenticationService } from './authentication.service';
import { User } from './_models/user.model';

@Injectable()
export class UserService {

    constructor(
        private http: Http,
        private auth: AuthenticationService) {}

    getUsers(): Promise<User[]> {
        const headers = new Headers({ 'Authorization': 'Bearer ' + this.auth.token });
        const options = new RequestOptions({headers});

        return this.http.get('/api/users', options)
            .toPromise()
            .then((res: Response) => res.json() as User[]);
    }

}
