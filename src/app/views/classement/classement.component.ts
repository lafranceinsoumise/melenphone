import { Component, OnInit } from '@angular/core';

import { LeaderboardService, LeaderboardApiData } from '../../shared';

@Component({
  selector: 'jlm-classement',
  templateUrl: './classement.component.html',
  styleUrls: ['./classement.component.scss']
})
export class ClassementComponent implements OnInit {
  leaderboards: LeaderboardApiData;

  constructor(private leaderboardService: LeaderboardService) { }

  ngOnInit() {
    this.leaderboardService.getLeaderboards()
      .then(leaderboards => this.leaderboards = leaderboards)
      .catch(err => console.trace(err));
  }

}
