import { Component, OnInit, Input } from '@angular/core';
import {
  trigger,
  state,
  style,
  transition,
  animate } from '@angular/core';
import { WsCallNotification } from '../../core';

@Component({
  selector: 'g[jlmAnimatedCall]',
  template: `
    <!--<svg:line *ngIf="callDescription"
        [attr.x1]="callDescription.caller.svg.x"
        [attr.y1]="callDescription.caller.svg.y"
        [attr.x2]="callDescription.callee.svg.x"
        [attr.y2]="callDescription.callee.svg.y"
        />-->
    <svg:path [attr.d]="getPathDescription(callDescription, 'curve')"/>
  `,
  styles: [`
    line, path {
      fill: transparent;
      stroke: firebrick;
      stroke-width: 6px;
      stroke-dasharray: 14px 10px;
      stroke-linecap: round;
    }
  `]
})
export class AnimatedCallComponent implements OnInit {

  @Input()
  callDescription: WsCallNotification;

  constructor() { }

  getPathDescription(desc: WsCallNotification, pathType: 'line' | 'curve') {
    const callerSvg = desc.caller.svg;
    const calleeSvg = desc.callee.svg;
    const delta = {
      x: calleeSvg.x - callerSvg.x,
      y: calleeSvg.y - callerSvg.y
    };
    switch (pathType) {
      case 'line':
        return `
          M ${callerSvg.x}, ${callerSvg.y}
          L ${calleeSvg.x}, ${calleeSvg.y}
          `;
      case 'curve':
        return getQuadraticCurve(callerSvg.x, callerSvg.y, calleeSvg.x, calleeSvg.y, .2);
    }

    function getQuadraticCurve(x1: number, y1: number, x2: number, y2: number, multiplier = .5): string {
      const [vecX, vecY] = [x2 - x1, y2 - y1];
      const [orthX, orthY] = [-vecY, vecX];
      const [deviationX, deviationY] = [orthX * multiplier, orthY * multiplier];
      const [step0x, step0y] = [x1, y1];
      const [vec1x, vec1y] = [vecX / 2 + deviationX, vecY / 2 + deviationY];


      return `
        M ${step0x} ${step0y}
        Q ${step0x + vec1x} ${step0y + vec1y} ${x2} ${y2} 
      `;
    }
  }

  ngOnInit() {
  }

}
