import { Component, OnInit, Input } from '@angular/core';

import { Achievement } from '../../shared/_models/achievement';

@Component({
  selector: 'jlm-achievement',
  templateUrl: './achievement.component.html',
  styleUrls: ['./achievement.component.scss']
})
export class AchievementComponent implements OnInit {
  @Input() trophy: Achievement = {
    codeName: 'count_animateur',
    condition: 'faire 29 lorem ipsum ipso facto bla bla bla Vladimir Poutine',
    name: 'name of the Achievement',
    phi: 20
  };

  constructor() { }

  ngOnInit() {
  }

}
