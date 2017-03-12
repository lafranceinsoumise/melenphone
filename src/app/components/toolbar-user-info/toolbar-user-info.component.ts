import { Component, OnInit, Input } from '@angular/core';

import { User } from '../../shared/_models/user.model';

@Component({
  selector: 'jlm-toolbar-user-info',
  templateUrl: './toolbar-user-info.component.html',
  styleUrls: ['./toolbar-user-info.component.scss']
})
export class ToolbarUserInfoComponent {

  @Input()
  user: User;

}
