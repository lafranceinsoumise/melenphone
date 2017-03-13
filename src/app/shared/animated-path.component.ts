import {
  Component,
  OnInit,
  Input,
  ViewChild,
  HostBinding,
  HostListener,
  ElementRef,
  ViewRef,
  AnimationStyles,
  AfterViewInit,
  AfterViewChecked,
  AnimationKeyframe
} from '@angular/core';

import { MapService } from './map.service';

@Component({
  selector: 'g[jlmAnimatedPath]',
  styles: [`
    path {
      transform-origin: center;
      fill: inherit;
    }
  `],
  template: `
    <svg:path #path [attr.d]="jlmAnimatedPath"
        [style.stroke-dasharray]="strokeDasharray"
        [style.stroke-dashoffset]="strokeDashoffset"
        [style.transition]="transition"/>
  `,
})
export class AnimatedPathComponent implements AfterViewInit {
  @ViewChild('path') pathEl: ViewRef;
  length: number;

  @Input('jlmAnimatedPath')
  jlmAnimatedPath: string;

  @Input() transitionTiming = '5s';
  @Input() from = -1;
  @Input() to = 0;

  @HostBinding('style.display') display = 'none';
  @HostBinding('class.transition-start') transitionStart = false;
  @HostBinding('class.transition-end') transitionEnd = false;
  strokeDasharray: string;
  strokeDashoffset: string;
  transition: string;

  constructor(private mapService: MapService) {}

  ngAfterViewInit() {
    this.length = this.pathEl['nativeElement'].getTotalLength();
    if (this.mapService.firstTime) {
      this.playAnimation();
    } else {
      this.strokeDasharray = null;
      this.strokeDashoffset = null;
      this.display = 'inline';
    }
  }

  playAnimation() {
    setTimeout(() => {
      this.display = 'inline';
      this.strokeDasharray = `${this.length}`;
      this.transitionStart = false;
      this.transitionEnd = false;
      this.strokeDashoffset = `${this.length * -this.from}`;
      this.transition = '';

      setTimeout(() => {
        this.transitionStart = true;
        this.strokeDashoffset = `${this.length * -this.to}`;
        this.transition = `stroke-dashoffset ${this.transitionTiming} linear, transform ${this.transitionTiming} linear`;
      });
    });

  }

}
