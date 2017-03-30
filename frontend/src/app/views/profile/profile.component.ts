import { Component, OnInit } from '@angular/core';

import { AuthenticationService, CallhubService } from '../../shared';

@Component({
  selector: 'jlm-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {

  callhubUsername = '';

  constructor(public auth: AuthenticationService, private callhubService: CallhubService) { }

  createCallhubAccount(name: string) {
    return this.callhubService.createCallhubAccount(name);
  }

}
