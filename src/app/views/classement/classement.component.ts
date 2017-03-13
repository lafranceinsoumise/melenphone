import { Component, OnInit } from '@angular/core';

import { LeaderboardService, LeaderboardApiData } from '../../shared';

@Component({
  selector: 'jlm-classement',
  templateUrl: './classement.component.html',
  styleUrls: ['./classement.component.scss']
})
export class ClassementComponent implements OnInit {
  rows: LeaderboardApiData;

  constructor(private leaderboardService: LeaderboardService) { }

  ngOnInit() {
    this.leaderboardService.getDaily()
      .then(leaderboard => this.rows = leaderboard)
      .catch(err => console.trace(err));
  }

}
