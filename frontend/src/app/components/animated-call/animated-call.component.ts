import { Component, OnInit, Input, ViewEncapsulation, ChangeDetectionStrategy } from '@angular/core';
import { WsCallNotification } from '../../core';

@Component({
  selector: 'g[jlmAnimatedCall]',
  template: `
    <svg:g>
      <svg:g class="call"
          *ngIf="pathInstructions"
          [jlmAnimatedPath]="pathInstructions"
          [transitionTiming]="'1s 2.5s'"
          [to]="1"/>

      <svg:circle class="caller1"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="1em"/>

      <svg:circle class="caller2"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="1em"/>

      <svg:circle class="caller3"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="0.75em"/>

      <svg:circle class="caller4"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="1em"/>

      <svg:circle class="caller5"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="1.25em"/>

      <svg:circle class="caller6"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.caller.svg)"
          [attr.cx]="jlmAnimatedCall.caller.svg.x"
          [attr.cy]="jlmAnimatedCall.caller.svg.y"
          r="1.5em"/>

      <svg:circle class="callee1"
          [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.callee.svg)"
          [attr.cx]="jlmAnimatedCall.callee.svg.x"
          [attr.cy]="jlmAnimatedCall.callee.svg.y"
          r="0.75em"/>

      <svg:circle class="callee2"
            [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.callee.svg)"
            [attr.cx]="jlmAnimatedCall.callee.svg.x"
            [attr.cy]="jlmAnimatedCall.callee.svg.y"
            r="1em"/>

      <svg:circle class="callee3"
            [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.callee.svg)"
            [attr.cx]="jlmAnimatedCall.callee.svg.x"
            [attr.cy]="jlmAnimatedCall.callee.svg.y"
            r="1.25em"/>

      <svg:circle class="callee4"
            [style.transform-origin]="getTransformOrigin(jlmAnimatedCall.callee.svg)"
            [attr.cx]="jlmAnimatedCall.callee.svg.x"
            [attr.cy]="jlmAnimatedCall.callee.svg.y"
            r="1.5em"/>
    </g>
  `,
  styleUrls: ['./animated-call.component.scss']
})
export class AnimatedCallComponent implements OnInit {

  pathInstructions: string;

  @Input()
  jlmAnimatedCall: WsCallNotification;

  constructor() { }

  getPathInstructions(desc: WsCallNotification, pathType: 'line' | 'curve') {
    const callerSvg = desc.caller.svg,
          calleeSvg = desc.callee.svg,
          delta = {
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

      const curvePath = `
        M ${step0x} ${step0y}
        Q ${step0x + vec1x} ${step0y + vec1y} ${x2} ${y2}
      `;

      return curvePath;
    }
  }

  getTransformOrigin(center: {x: number, y: number}) {
    return `${ center.x }px ${ center.y }px`;
  }

  ngOnInit() {
    this.pathInstructions = this.getPathInstructions(this.jlmAnimatedCall, 'curve');
  }

}
