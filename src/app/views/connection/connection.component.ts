import { Component, OnInit } from '@angular/core';

import { AuthenticationService } from '../../shared/authentication.service';

@Component({
  selector: 'jlm-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent {

  callhubUsername = '';

  constructor(private auth: AuthenticationService) { }

  createCallhubAccount(name: string) {
    console.log('@TODO : call callhub API');
  }

}
