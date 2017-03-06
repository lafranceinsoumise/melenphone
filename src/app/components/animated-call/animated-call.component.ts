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
    <svg:path [attr.d]="getPathDescription(jlmAnimatedCall, 'curve')"/>
    <svg:circle class="caller" [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
        [attr.cx]="jlmAnimatedCall.caller.svg.x"
        [attr.cy]="jlmAnimatedCall.caller.svg.y"
        r="2em"/>
    <svg:circle class="callee" [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.callee.svg)"
        [attr.cx]="jlmAnimatedCall.callee.svg.x"
        [attr.cy]="jlmAnimatedCall.callee.svg.y"
        r="2em"/>
  `,
  styles: [`
    line, path {
      fill: transparent;
      stroke: firebrick;
      stroke-width: 6px;
      stroke-dasharray: 14px 10px;
      stroke-linecap: round;
    }

    circle {
      fill: rgba(0,0,0,.2);
      animation: zoomIn 1s;
    }

    circle.callee {
      animation: zoomIn 1s .2s;
      animation-fill-mode: both;
    }

    @keyframes zoomIn {
      from {
        transform: scale(0);
      }
      80% {
        transform: scale(1.2);
      }
      to {
        transform: scale(1);
      }
    }
  `]
})
export class AnimatedCallComponent implements OnInit {

  @Input()
  jlmAnimatedCall: WsCallNotification;

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

  getTransformOrigin(center: {x: number, y: number}) {
    return `${ center.x }px ${ center.y }px`;
  }

  ngOnInit() {
  }

}
