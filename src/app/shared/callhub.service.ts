import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { CallhubUser } from './_models';
import { AuthenticationService } from './';

@Injectable()
export class CallhubService {
  currentUser: CallhubUser = null;

  constructor(
    private http: Http,
    private auth: AuthenticationService) { }

  createCallhubAccount(agentUsername: string): Promise<CallhubUser> {
    return this.http.post('/api/current_user/caller_information', {agentUsername})
      .toPromise()
      .then((res: Response) => {
        if (res.status === 400) {
          throw res.json();
        } else if (res.status === 201) {
          this.currentUser = res.json() as CallhubUser;
          this.auth.currentUser.agentUsername = this.currentUser.agentUsername;
          this.auth.currentUser.phi = this.currentUser.phi;
          return this.currentUser;
        }
      })
      .catch(err => {
        throw err;
      });
  }

  associateExistingAgent(agentUsername: string, password: string): Promise<CallhubUser> {
    return this.http.post('/api/current_user/associate_existing_agent', {agentUsername, password})
      .toPromise()
      .then((res: Response) => {
        if (res.status === 400) {
          throw res.json();
        } else if (res.status === 201) {
          this.currentUser = res.json() as CallhubUser;
          this.auth.currentUser.agentUsername = this.currentUser.agentUsername;
          this.auth.currentUser.phi = this.currentUser.phi;
          return this.currentUser;
        }
      })
      .catch(err => {
        throw err;
      });
  }

}
