import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { CallNoteDescription } from './core';
import {
  SocketConnectionService,
  AuthenticationService
} from './shared';

@Component({
  selector: 'jlm-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  dailyCalls = 0;
  get goal() {
    return this.chooseCallGoal(this.dailyCalls || 0);
  }

  constructor(
    private scs: SocketConnectionService,
    private auth: AuthenticationService,
    private http: Http
  ) {}

  ngOnInit() {
    this.auth.getProfile()
      .catch(err => console.error(err.json()));
    this.scs.room.addEventListener('message', (event) =>
      this.onNotif(event)
    , false);
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
    const parsed = JSON.parse(message.data);
    switch (parsed.type) {
      case 'call':
        const notif = parsed.value as CallNoteDescription;
        this.dailyCalls = notif.updatedData.dailyCalls;
        if (
          this.auth.currentUser !== null
          && this.auth.currentUser.agentUsername === notif.call.caller.agentUsername
        ) {
          this.auth.getExtendedInfo()
            .then((info) => {
              this.auth.currentUser.phi = info.phi;
            });
        }
      break;
      case 'achievement':
      break;
    }
  }

  chooseCallGoal(callCount) {
    const sizes = [10, 50, 100, 250, 500, 1000, 2000, 5000, 10000, 50000];
    for (const value of sizes) {
      if (callCount < 0.95 * value) {
          return value;
      }
    }
    return (1000000000000);
  }

}
