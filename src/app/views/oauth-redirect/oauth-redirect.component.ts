import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MdSnackBar } from '@angular/material';

import { AuthenticationService, CallhubService, User, CallhubUser } from '../../shared';

@Component({
  selector: 'jlm-oauth-redirect',
  templateUrl: './oauth-redirect.component.html',
  styleUrls: ['./oauth-redirect.component.scss']
})
export class OauthRedirectComponent implements OnInit {
  message: string = null;
  newAgent = {
    credentials: {
      username: null,
      password: null
    },
    isPending: false,
    errorMessage: null
  };
  existingAgent = {
    credentials: {
      username: null,
      password: null
    },
    isPending: false,
    errorMessage: null
  };
  errorMessage = null;
  pendingRequest = false;

  get shouldDisableSubmitButton() {
    const res = this.pendingRequest ||
        this.newAgent.credentials.username == null ||
        (this.newAgent.credentials.username !== null && this.newAgent.credentials.username.length < 4);
    return res;
  }

  constructor(
    private auth: AuthenticationService,
    private callhub: CallhubService,
    private snackBar: MdSnackBar,
    private router: Router) { }

  ngOnInit() {
    this.auth.getProfile()
      .then((user: User) => {
        if (user !== null) {
          if (user.agentUsername === null) {
            this.message = 'createCallhubAccount';
          } else {
            this.message = 'normal';
            this.snackBar.open('Connexion avec le QG de la France Insoumise établie 🚀', undefined, {
              duration: 4000
            });
            this.router.navigate(['/']);
          }
        }
      });
  }

  createCallhubAccount(newAgentUserName: string): Promise<CallhubUser> {
    console.group('Callhub agent creation request');
    this.newAgent.isPending = true;

    return this.callhub.createCallhubAccount(newAgentUserName)
      .then((user) => {
        console.table(user);
        this.newAgent.isPending = false;
        this.snackBar.open('Compte Callhub créé avec succès 🚀', undefined, { duration: 4000 });
        this.message = 'checkYourMailbox';
        console.groupEnd();
        return user;
      })
      .catch((err) => {
        console.error(err);
        this.newAgent.isPending = false;
        this.newAgent.errorMessage = err.json().detail;
        this.snackBar.open(this.newAgent.errorMessage, undefined, { duration: 4000 });
        console.groupEnd();
      });
  }

  associateExistingAgent(username: string, password: string) {
    this.existingAgent.isPending = true;
    return this.callhub.associateExistingAgent(username, password)
      .then((result: any) => {
        this.existingAgent.isPending = false;
        console.log(result);
        this.snackBar.open('le compte a été récupéré avec succès.');
      })
      .catch((err) => {
        this.existingAgent.isPending = false;
        console.log('erreur durant l\'association de compte');
      });
  }

}
