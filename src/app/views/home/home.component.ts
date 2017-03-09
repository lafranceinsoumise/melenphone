import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import { CoordinatesConverterService, SocketConnectionService } from '../../shared';
import 'rxjs/add/operator/toPromise';
import { WsCallNotification } from '../../core';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  constructor(
    private coordsConverter: CoordinatesConverterService,
    private wsc: SocketConnectionService,
    private http: Http) { }

  makeBackendRequest() {
    this.http.post('/api/simulate_call', '')
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
