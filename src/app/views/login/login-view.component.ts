import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'jlm-login',
  template: `
    <div>
      Please enter your login and password
      <input md-input type="text">
    </div>
  `,
  styleUrls: ['./login-view.component.scss']
})
export class LoginComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
