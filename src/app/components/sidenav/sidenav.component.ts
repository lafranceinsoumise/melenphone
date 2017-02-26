import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'jlm-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent implements OnInit {
  links = [
    { path: '/', text: 'Carte' },
    { path: '/pokechon', text: 'pokéchon' }
  ];
  constructor() { }

  ngOnInit() {
  }

}
