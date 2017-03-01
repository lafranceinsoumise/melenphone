import { Component, OnInit } from '@angular/core';
import { RiriComponent, FifiComponent, LoulouComponent } from '../../components/widgets';
import { CoordinatesConverterService } from '../../shared/coordinates-converter.service';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  lilDucks: {component: any, inputs: Object}[] = [];

  constructor(private coordsConverter: CoordinatesConverterService) { }

  ngOnInit() {
    console.log(this.coordsConverter.getSvgLocation(48.577725, 7.738060));
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
