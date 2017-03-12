import { Component, OnInit } from '@angular/core';

import { AuthenticationService } from './shared/authentication.service';

@Component({
  selector: 'jlm-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  constructor(private auth: AuthenticationService) {}

  ngOnInit() {
    this.auth.getProfile()
      .catch(err => console.error(err.json()));
  }

}
