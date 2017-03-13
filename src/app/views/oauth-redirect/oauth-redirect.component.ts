import { Component, OnInit } from '@angular/core';

import { AuthenticationService } from '../../shared';

@Component({
  selector: 'jlm-oauth-redirect',
  templateUrl: './oauth-redirect.component.html',
  styleUrls: ['./oauth-redirect.component.scss']
})
export class OauthRedirectComponent implements OnInit {

  constructor(private auth: AuthenticationService) { }

  ngOnInit() {
    // this.auth.currentUser
  }

}
