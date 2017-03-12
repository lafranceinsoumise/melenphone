import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from '../../shared/authentication.service';

interface Credentials {
  username: string;
  password: string;
}

@Component({
  selector: 'jlm-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  credentials: Credentials = {
    username: null,
    password: null
  };
  loading = false;
  error = '';

  constructor(
    private router: Router,
    private auth: AuthenticationService
  ) { }

  ngOnInit() {
  }

}
