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
    const sentObject: WsCallNotification = {
      caller: {
        gps: {
          // Ajaccio
          lat: 41.919322,
          lng: 8.738221
        }
      },
      callee: {
        gps: {
          // Bordeaux
          lat: 44.833328,
          lng: -0.56667
        }
      },
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
