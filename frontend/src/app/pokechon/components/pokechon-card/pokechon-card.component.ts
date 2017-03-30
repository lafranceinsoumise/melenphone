import { Component, OnInit, Input } from '@angular/core';
import { PokechonCardInfo } from '../../common';

@Component({
  selector: 'jlm-pokechon-card',
  templateUrl: './pokechon-card.component.html',
  styleUrls: ['./pokechon-card.component.scss']
})
export class PokechonCardComponent implements OnInit {
  @Input() cardInfo: PokechonCardInfo;

  constructor() { }

  ngOnInit() {
  }

}
