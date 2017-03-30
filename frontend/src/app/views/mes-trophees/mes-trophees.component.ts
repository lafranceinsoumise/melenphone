import { Component, OnInit } from '@angular/core';

import { UserService, AchievementApiData } from '../../shared';

@Component({
  selector: 'jlm-mes-trophees',
  templateUrl: './mes-trophees.component.html',
  styleUrls: ['./mes-trophees.component.scss']
})
export class MesTropheesComponent implements OnInit {
  trophiesData: AchievementApiData;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.userService.getCurrentUserAchievements()
      .then((trophiesData: AchievementApiData) => {
        this.trophiesData = trophiesData;
      });
  }

}
