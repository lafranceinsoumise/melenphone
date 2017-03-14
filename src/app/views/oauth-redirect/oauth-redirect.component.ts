import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

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

  constructor(
    private auth: AuthenticationService,
    private callhub: CallhubService,
    private router: Router) { }

  ngOnInit() {
    this.auth.getProfile()
      .then((user: User) => {
        if (user !== null) {
          if (user.agentUsername === null) {
            this.shouldDisplayCallhubForm = true;
          } else {
            this.shouldDisplayNormalMessage = true;
            setTimeout(() => this.router.navigate(['/']), 500);
          }
        }
      });
  }

  createCallhubAccount(callhubUsername: string): Promise<CallhubUser> {
    return this.callhub.createCallhubAccount(callhubUsername)
      .then((user) => {
        this.router.navigate(['/']);
        return user;
      })
      .catch((err) => {
        console.trace(err);
        this.errorMessage = err;
      });
  }

}
