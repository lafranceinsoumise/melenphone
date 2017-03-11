import {
  Component,
  OnInit,
  Input,
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
  selector: 'path[jlmAnimatedPath]',
  styles: [`
    :host {
      transform-origin: center;
      display; none;
    }
    :host.transition-start {
      // transform: scale(.8);
    }
    :host.transition-end {
      // transform: scale(1);
    }
  `],
  template: '',
})
export class AnimatedPathComponent implements AfterViewInit {
  length: number;

  @Input('jlmAnimatedPath')
  @HostBinding('attr.d')
  jlmAnimatedPath: string;

  @Input() transitionTiming = '5s';

  @HostBinding('style.display') display = 'none';
  @HostBinding('style.stroke-dasharray') strokeDasharray: string;
  @HostBinding('style.stroke-dashoffset') strokeDashoffset: string;
  @HostBinding('style.transition') transition: string;
  @HostBinding('class.transition-start') transitionStart = false;
  @HostBinding('class.transition-end') transitionEnd = false;

  constructor(private host: ElementRef) {}

  ngAfterViewInit() {
    this.length = this.host.nativeElement.getTotalLength();
    setTimeout(() => this.playAnimation());
  }

  playAnimation() {
    this.display = 'inline';
    this.strokeDasharray = `${this.length}`;
    this.strokeDashoffset = `${this.length}`;
    this.transition = '';
    this.transitionStart = true;
    this.transitionEnd = false;

    setTimeout(() => {
      this.strokeDashoffset = '0';
      this.transition = `stroke-dashoffset ${this.transitionTiming} linear, transform ${this.transitionTiming} linear`;
      this.transitionStart = false;
      this.transitionEnd = true;
    });
  }

}
