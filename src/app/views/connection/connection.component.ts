import { Component, OnInit } from '@angular/core';

import { AuthenticationService, CallhubService } from '../../shared';

@Component({
  selector: 'jlm-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent {

  callhubUsername = '';

  constructor(private auth: AuthenticationService, private callhubService: CallhubService) { }

  createCallhubAccount(name: string) {
    return this.callhubService.createCallhubAccount(name);
  }

}
