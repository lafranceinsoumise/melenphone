import { Component, OnInit } from '@angular/core';
import { RiriComponent, FifiComponent, LoulouComponent } from '../../components/widgets';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  lilDucks: {component: any, inputs: Object}[] = [];

  constructor() { }

  ngOnInit() {
  }

  createRiriComponent() {
    this.lilDucks.push({
      component: RiriComponent,
      inputs: {
        showNum: 9
      }
    });
  }

  createFifiComponent() {
    this.lilDucks.push({
      component: FifiComponent,
      inputs: {
        showNum: 10
      }
    });
  }

  createLoulouComponent() {
    this.lilDucks.push({
      component: LoulouComponent,
      inputs: {
        showNum: 11
      }
    });
  }

}
