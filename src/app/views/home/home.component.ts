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
    this.wsc.room.addEventListener('message', (event) => console.log(event));
    this.wsc.room.addEventListener('open', (event) => console.log(event));
    this.wsc.room.addEventListener('error', (event) => console.log(event));
    this.wsc.room.addEventListener('close', (event) => console.log(event)); 
  }

  makeBackendRequest() {
    const sentObject = {
      name: 'Robert',
      lastName: 'Baratheon',
      gps: {
        lat: ' 48.866667',
        lng: '2.33'
      }
    };
    return this.http.post('/api/test_websocket/', sentObject)
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error(`erreur de communication avec le serveur : ${res.status}`);
        }
        return res.json();
      })
      .catch(error => console.error(error));
  }

}
