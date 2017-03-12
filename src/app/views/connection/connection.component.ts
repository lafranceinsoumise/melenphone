import { Component, OnInit } from '@angular/core';

import { AuthenticationService } from '../../shared/authentication.service';

@Component({
  selector: 'jlm-connection',
  templateUrl: './connection.component.html',
  styleUrls: ['./connection.component.scss']
})
export class ConnectionComponent implements OnInit {

  constructor(private auth: AuthenticationService) { }

  ngOnInit() {
    this.auth.getProfile();
  }

}
