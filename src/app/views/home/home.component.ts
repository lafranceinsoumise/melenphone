import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import { CoordinatesConverterService, SocketConnectionService, AuthenticationService } from '../../shared';
import 'rxjs/add/operator/toPromise';
import { WsCallNotification, CallNoteDescription } from '../../core';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  dailyCalls = 0;
  goal: 200;

  constructor(
    private coordsConverter: CoordinatesConverterService,
    private scs: SocketConnectionService,
    private auth: AuthenticationService,
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

  ngOnInit() {
    this.scs.room.addEventListener('message', (event) => this.onNotif(event), false);
    this.http.get('/api/basic_information')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error(`erreur de communication avec le serveur : ${res.status}`);
        }

        this.dailyCalls = res.json()['dailyCalls'];
      })
      .catch(error => console.error(error));
  }

  onNotif(message: MessageEvent) {
    const notif = JSON.parse(message.data) as CallNoteDescription;
    this.dailyCalls = notif.updatedData.dailyCalls;
    if (this.auth.currentUser !== null && this.auth.currentUser.agentUsername === notif.call.caller.agentUsername) {
      this.auth.currentUser.phi += 10;
    }
  }

}
