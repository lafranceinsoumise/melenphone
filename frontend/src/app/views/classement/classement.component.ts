import { Component, OnInit } from '@angular/core';

import { BasicService, LeaderboardService, LeaderboardApiData } from '../../shared';

@Component({
  selector: 'jlm-classement',
  templateUrl: './classement.component.html',
  styleUrls: ['./classement.component.scss']
})
export class ClassementComponent implements OnInit {
  leaderboards: LeaderboardApiData;

  constructor(
    private basic: BasicService,
    private leaderboardService: LeaderboardService,
  ) { }

  ngOnInit() {
    console.log(this.basic);
    this.leaderboardService.getLeaderboards()
      .then(leaderboards => this.leaderboards = leaderboards)
      .catch(err => console.trace(err));
  }

}
