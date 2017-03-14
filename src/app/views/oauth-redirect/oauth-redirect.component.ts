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
  shouldDisplayNormalMessage = false;
  callhubUsername = null;
  errorMessage = null;
  pendingRequest = false;

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
            this.shouldDisplayCallhubForm = true;
          } else {
            this.shouldDisplayNormalMessage = true;
            this.snackBar.open('Connexion avec le QG de la France Insoumise établie 🚀');
            this.router.navigate(['/']);
          }
        }
      });
  }

  createCallhubAccount(callhubUsername: string): Promise<CallhubUser> {
    this.pendingRequest = true;

    return this.callhub.createCallhubAccount(callhubUsername)
      .then((user) => {
        this.snackBar.open('Compte Callhub créé avec succès 🚀');
        this.router.navigate(['/']);
        return user;
      })
      .catch((err) => {
        this.pendingRequest = false;
        this.errorMessage = err.detail;
        this.snackBar.open(this.errorMessage);
      });
  }

}
