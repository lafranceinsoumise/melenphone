import { Component, OnInit } from '@angular/core';
import { CoordinatesConverterService, SocketConnectionService } from '../../shared';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  lilDucks: {component: any, inputs: Object}[] = [];

  constructor(private coordsConverter: CoordinatesConverterService, private wsc: SocketConnectionService) { }

  ngOnInit() {
    console.log(this.coordsConverter.getSvgLocation(48.577725, 7.738060));

    this.wsc.room.addEventListener('message', (event) => console.log(event), false);
  }

}
