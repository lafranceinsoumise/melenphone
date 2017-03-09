import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';

interface RegistrationInformations {
  username: string;
  email: string;
  password: string;
  passwordConfirmation: string;
  country: string;
  city: string;
}

@Component({
  selector: 'jlm-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  formInfo: RegistrationInformations;

  constructor() { }

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

  sendInformations(values) {
    console.log(values);
  }

}
