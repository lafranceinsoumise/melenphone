import { Component, OnInit, Input } from '@angular/core';
import { WsCallNotification } from '../../core';

@Component({
  selector: 'g[jlmAnimatedCall]',
  template: `
    <svg:line *ngIf="callDescription"
        [attr.x1]="callDescription.caller.svg.x"
        [attr.y1]="callDescription.caller.svg.y"
        [attr.x2]="callDescription.callee.svg.x"
        [attr.y2]="callDescription.callee.svg.y"
        />
  `,
  styles: [`
    line {
      stroke: firebrick;
      stroke-width: 4;

    }
  `]
})
export class AnimatedCallComponent implements OnInit {

  @Input()
  callDescription: WsCallNotification;

  constructor() { }

  ngOnInit() {
  }

}
