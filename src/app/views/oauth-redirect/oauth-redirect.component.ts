import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from '../../shared';

@Component({
  selector: 'jlm-oauth-redirect',
  templateUrl: './oauth-redirect.component.html',
  styleUrls: ['./oauth-redirect.component.scss']
})
export class OauthRedirectComponent implements OnInit {
  shouldDisplayCallhubForm = false;
  shouldDisplayNormalMessage = false;

  constructor(private auth: AuthenticationService, private router: Router) { }

  ngOnInit() {
    this.auth.getProfile()
      .then(() => {
        if (this.auth.currentUser !== null) {
          if (this.auth.currentUser.agentUsername === null) {
            this.shouldDisplayCallhubForm = true;
          } else {
            this.shouldDisplayNormalMessage = true;
            this.router.navigate(['/']);
          }
        }
      });
  }

}
