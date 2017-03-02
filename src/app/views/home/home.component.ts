import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import { CoordinatesConverterService, SocketConnectionService } from '../../shared';
import 'rxjs/add/operator/toPromise';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  lilDucks: {component: any, inputs: Object}[] = [];

  constructor(
    private coordsConverter: CoordinatesConverterService,
    private wsc: SocketConnectionService,
    private http: Http) { }

  ngOnInit() {
    console.log(this.coordsConverter.getSvgLocation(48.577725, 7.738060));

    this.wsc.room.addEventListener('message', (event) => {
      console.log(event);
    });

    this.wsc.room.addEventListener('open', (event) => {
      console.log(event);
    });

    this.wsc.room.addEventListener('error', (event) => {
      console.log(event);
    });

    this.wsc.room.addEventListener('close', (event) => {
      console.log(event);
    });
  }

  makeBackendRequest() {
    const sentObject = {
      name: 'Robert',
      lastName: 'Baratheon',
      gps: {
        lat: '55',
        lng: '40'
      }
    };
    this.http.post('/api/test_websocket/', sentObject)
      .toPromise()
      .then((res: Response) => {
        console.log('[POST] api/test_websocket/ ', res.status);
        res.json();
      })
      .catch(error => console.error(error));
  }

}
