import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'jlm-topten',
  templateUrl: './topten.component.html',
  styleUrls: ['./topten.component.scss']
})
export class ToptenComponent implements OnInit {

  @Input() dailyLeaderboard;

  constructor() { }

  ngOnInit() {
  }

}
