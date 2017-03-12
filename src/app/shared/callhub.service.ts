import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { CallhubUser } from './_models/user.model';

@Injectable()
export class CallhubService {
  currentUser: CallhubUser = null;

  constructor(private http: Http) { }

  createCallhubAccount(agentUsername: string): Promise<CallhubUser> {
    return this.http.post('/api/current_user/caller_information', {agentUsername})
      .toPromise()
      .then((res: Response) => {
        if (res.status === 400) {
          throw new Error('erreur lors de la création de l\agent callhub');
        } else if (res.status === 204) {
          this.currentUser = res.json() as CallhubUser;
          return this.currentUser;
        }
      })
      .catch((err) => {
        console.trace(err);
      });
  }

}
