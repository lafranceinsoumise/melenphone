import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from '../../shared/authentication.service';

interface Credentials {
  userName: string;
  password: string;
}

@Component({
  selector: 'jlm-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  credentials: Credentials = {
    userName: '',
    password: ''
  };
  loading = false;
  error = '';

  constructor(
    private router: Router,
    private auth: AuthenticationService
  ) { }

  ngOnInit() {
  }

  logout() {
    this.auth.logout();
  }

  login() {
    this.loading = true;
    this.auth.login(this.credentials.userName, this.credentials.password)
      .then((result) => {
        this.loading = false;
        if (result === true) {
          this.router.navigate(['/']);
        } else {
          this.error = `Le nom d'utilisateur ou le mot de passe est incorrect`;
        }
      });
  }

}
