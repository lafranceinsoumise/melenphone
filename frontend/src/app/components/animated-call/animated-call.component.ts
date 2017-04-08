import {
  Component,
  Input,
  ViewEncapsulation,
  ChangeDetectionStrategy
} from '@angular/core';

import { CallLocationDescription, Point } from '../../shared/_models';

@Component({
  selector: 'g[jlmAnimatedCall]',
  template: `
    <svg:g *ngIf="pathInstructions">
      <svg:g class="call"
          [jlmAnimatedPath]="pathInstructions"
          [transitionTiming]="'4s 0s'"
          [to]="1"/>

      <svg:circle *ngFor="let circleClassName of callerCircles; index as i"
          [attr.class]="'caller' + i"
          [style.transform-origin]="callerTransformOrigin"
          [attr.cx]="callerSvgCoordinates.x"
          [attr.cy]="callerSvgCoordinates.y"
          r="2em"/>

      <svg:circle *ngFor="let circleClassName of calleeCircles; index as i"
          [attr.class]="'callee' + i"
          [style.transform-origin]="calleeTransformOrigin"
          [attr.cx]="calleeSvgCoordinates.x"
          [attr.cy]="calleeSvgCoordinates.y"
          r="2em"/>
    </g>
  `,
  styleUrls: ['./animated-call.component.scss']
})
export class AnimatedCallComponent {

  pathInstructions: string;

  callerSvgCoordinates: Point;
  calleeSvgCoordinates: Point;

  callerTransformOrigin: string;
  calleeTransformOrigin: string;

  callerCircles = new Array(4);
  calleeCircles = new Array(4);

  @Input()
  get jlmAnimatedCall(): CallLocationDescription {
    return this._animatedCall;
  }
  set jlmAnimatedCall(call: CallLocationDescription) {
    this._animatedCall = call;
    this.pathInstructions = this.getPathInstructions(this.jlmAnimatedCall, 'curve');
    this.callerSvgCoordinates = call.caller.svg;
    this.calleeSvgCoordinates = call.callee.svg;
    this.callerTransformOrigin = this.getTransformOrigin(this.callerSvgCoordinates);
    this.calleeTransformOrigin = this.getTransformOrigin(this.calleeSvgCoordinates);
  }
  private _animatedCall: CallLocationDescription;

  getPathInstructions(desc: CallLocationDescription, pathType: 'line' | 'curve') {
    const callerSvg = desc.caller.svg,
          calleeSvg = desc.callee.svg,
          delta     = {
            x: calleeSvg.x - callerSvg.x,
            y: calleeSvg.y - callerSvg.y
          };

    switch (pathType) {
      case 'line':
        return getLineCurve(callerSvg, calleeSvg);
      case 'curve':
        return getQuadraticCurve(callerSvg, calleeSvg, .2);
    }

    function getLineCurve(origin: Point, destination: Point): string {
      const curvePath = `
          M ${origin.x}, ${origin.y}
          L ${destination.x}, ${destination.y}
          `;
      return curvePath;
    }

    function getQuadraticCurve(origin: Point, destination: Point, multiplier = .5): string {
      const [vecX, vecY] = [destination.x - origin.x, destination.y - origin.y];
      const [orthX, orthY] = [-vecY, vecX];
      const [deviationX, deviationY] = [orthX * multiplier, orthY * multiplier];
      const [step0x, step0y] = [origin.x, origin.y];
      const [vec1x, vec1y] = [vecX / 2 + deviationX, vecY / 2 + deviationY];

      const curvePath = `
        M ${step0x} ${step0y}
        Q ${step0x + vec1x} ${step0y + vec1y} ${destination.x} ${destination.y}
      `;

      return curvePath;
    }
  }

  getTransformOrigin(center: Point) {
    return `${ center.x }px ${ center.y }px`;
  }

}
