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
  shouldDisplayCallhubForm = false;
  message: string = null;
  callhubUsername = null;
  errorMessage = null;
  pendingRequest = false;

  get shouldDisableSubmitButton() {
    const res = this.pendingRequest ||
        this.callhubUsername == null ||
        (this.callhubUsername !== null && this.callhubUsername.length < 4);
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

  createCallhubAccount(callhubUsername: string): Promise<CallhubUser> {
    console.group('Callhub agent creation request');
    this.pendingRequest = true;

    return this.callhub.createCallhubAccount(callhubUsername)
      .then((user) => {
        console.table(user);
        this.snackBar.open('Compte Callhub créé avec succès 🚀', undefined, { duration: 4000 });
        this.message = 'checkYourMailbox';
        console.groupEnd();
        return user;
      })
      .catch((err) => {
        console.error(err);
        this.pendingRequest = false;
        this.errorMessage = err.json().detail;
        this.snackBar.open(this.errorMessage, undefined, { duration: 4000 });
        console.groupEnd();
      });
  }

}
