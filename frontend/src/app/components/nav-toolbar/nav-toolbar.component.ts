import { Component, OnInit, Input } from '@angular/core';

import { User } from '../../shared/_models/user.model';

@Component({
  selector: 'jlm-nav-toolbar',
  templateUrl: './nav-toolbar.component.html',
  styleUrls: ['./nav-toolbar.component.scss']
})
export class NavToolbarComponent {

  @Input()
  user: User;

}
