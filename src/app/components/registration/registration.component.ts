import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';

import { UserService, RegistrationInformations } from '../../shared';

@Component({
  selector: 'jlm-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  formInfo: RegistrationInformations;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.reset();
  }

  reset(): void {
    this.formInfo = {
      username: '',
      email: '',
      password: '',
      passwordConfirmation: '',
      country: '',
      city: ''
    };
  }

  sendInformations(formValues: RegistrationInformations) {
    this.userService.register(formValues);
  }

}
