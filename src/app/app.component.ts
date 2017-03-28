import { Component, OnInit } from '@angular/core';
import { MdSnackBar, MdSnackBarConfig, MdSnackBarRef } from '@angular/material';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { CallNoteDescription } from './core';
import {
  SocketConnectionService,
  AuthenticationService,
  BasicService,
  BasicInformationApiData,
  Achievement,
  AchievementNotification
} from './shared';

import {
  AchievementComponent
} from './components';

@Component({
  selector: 'jlm-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  entryComponents: [ AchievementComponent ]
})
export class AppComponent implements OnInit {
  get goal() {
    return this.chooseCallGoal(this.basic.infos.dailyCalls || 0);
  }

  constructor(
    private scs: SocketConnectionService,
    public auth: AuthenticationService,
    private http: Http,
    public basic: BasicService,
    private snack: MdSnackBar,
  ) {}

  ngOnInit() {
    this.auth.getProfile()
      .catch(err => console.error(err.json()));
    this.scs.room.addEventListener('message', (event) =>
      this.onNotif(event)
    , false);
    this.basic.getBasicInfo()
      .then(infos => this.basic.infos = infos)
      .catch(err => console.trace(err));
  }

  onNotif(message: MessageEvent) {
    const parsed = JSON.parse(message.data);
    switch (parsed.type) {
      case 'call':
        const notif = parsed.value as CallNoteDescription;
        this.basic.infos = notif.updatedData;
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
        const trophyNotification = parsed as AchievementNotification;
        const trophy = trophyNotification.value.achievement;
        const winnerUsername = trophyNotification.value.agentUsername;
        const config: MdSnackBarConfig = { duration: 5000 };
        const ref = this.snack.openFromComponent(AchievementComponent, config);
        ref.instance.trophy = trophy;
        ref.instance.winnerUsername = winnerUsername;
      break;
    }
  }

  mockAchievement() {
    this.http.post('/api/simulate_achievement', {})
      .toPromise()
      .then(res => console.log(res.json()));
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
