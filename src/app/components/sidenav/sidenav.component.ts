import { Component } from '@angular/core';

@Component({
  selector: 'jlm-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent {
  links = [
    { path: '/', text: 'Carte' },
    { path: '/mes-trophees', text: 'Mes trophées' },
    { path: '/classement', text: 'Classement'}
  ];
  constructor() { }

}
