import {
  Component,
  Renderer,
  OnInit,
  Input,
  HostBinding,
  HostListener,
  ElementRef,
  ViewRef,
  AnimationStyles,
  AfterViewInit,
  AnimationKeyframe
} from '@angular/core';
import { animate, AnimationStyleMetadata, AnimationKeyframesSequenceMetadata } from '@angular/animations';

@Component({
  selector: 'path[jlmAnimatedPath]',
  styles: [`
    :host {
      transform-origin: center;
    }
    :host.transition-start {
      transform: scale(.8);
    }
    :host.transition-end {
      stroke-dashoffset: 0;
      transform: scale(1);
    }
  `],
  template: '',
})
export class AnimatedPathComponent implements AfterViewInit {
  length: number;

  @Input('jlmAnimatedPath')
  @HostBinding('attr.d')
  jlmAnimatedPath: string;

  @HostBinding('style.stroke-dasharray') strokeDasharray: number;
  @HostBinding('style.stroke-dashoffset') strokeDashoffset: string;
  @HostBinding('style.transition') transition: string;
  @HostBinding('class.transition-start') transitionStart = false;
  @HostBinding('class.transition-end') transitionEnd = false;

  constructor(private renderer: Renderer, private host: ElementRef) {}

  ngAfterViewInit() {
    this.length = this.host.nativeElement.getTotalLength();
    this.playAnimation();
  }

  @HostListener('click', [])
  playAnimation() {
    this.strokeDasharray = this.length;
    this.strokeDashoffset = `${-this.length}`;
    this.transition = '';
    this.transitionStart = true;
    this.transitionEnd = false;

    setTimeout(() => {
      this.transition = 'stroke-dashoffset 5s linear, transform 5s linear';
      this.transitionStart = false;
      this.transitionEnd = true;
      this.strokeDashoffset = '0';
    });
  }

}
