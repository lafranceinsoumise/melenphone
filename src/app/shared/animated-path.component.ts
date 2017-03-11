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

@Component({
  selector: 'g[jlmAnimatedPath]',
  styles: [`
    path {
      transform-origin: center;
      fill: transparent;
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

  constructor() {}

  ngAfterViewInit() {
    this.length = this.pathEl['nativeElement'].getTotalLength();
    this.playAnimation();
  }

  playAnimation() {
    setTimeout(() => {
      this.display = 'inline';
      this.strokeDasharray = `${this.length}`;
      this.strokeDashoffset = `${this.length * -this.from}`;
      this.transition = '';

      setTimeout(() => {
        this.strokeDashoffset = `${this.length * -this.to}`;
        this.transition = `stroke-dashoffset ${this.transitionTiming} linear, transform ${this.transitionTiming} linear`;
      });
    });

  }

}
