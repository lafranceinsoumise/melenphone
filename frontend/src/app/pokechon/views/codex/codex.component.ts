import { Component, OnInit } from '@angular/core';
import { PokechonCardService, PokechonCardInfo } from '../../common';

@Component({
  selector: 'jlm-codex',
  templateUrl: './codex.component.html',
  styleUrls: ['./codex.component.scss']
})
export class CodexComponent implements OnInit {
  cards: PokechonCardInfo[] = [];

  constructor(private pcs: PokechonCardService) { }

  ngOnInit() {
    this.pcs.getPokechonCards().then(pokechonCards => this.cards = pokechonCards);
  }

}
