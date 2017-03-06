import { 
  Component,
  Renderer,
  OnInit,
  Input,
  HostBinding,
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
      transition: stroke-dashoffset 2s;
      stroke-dashoffset: 0;
    }
  `],
  template: '',
})
export class AnimatedPathComponent implements AfterViewInit {
  length: number;

  @Input('jlmAnimatedPath')
  @HostBinding('attr.d')
  jlmAnimatedPath: string;

  @HostBinding('style.stroke-dasharray')
  strokeDasharray: number;

  @HostBinding('style.stroke-dashoffset')
  strokeDashOffset: string;

  constructor(private renderer: Renderer, private host: ElementRef) { }

  ngAfterViewInit() {
    this.strokeDasharray = this.host.nativeElement.getTotalLength();
    this.strokeDashOffset = `${-this.strokeDasharray}`;
    this.play();
  }

  play() {
    setTimeout(() => this.strokeDashOffset = '0', 1000);
    // const startingStyles = {
    //   styles: [{'stroke': 'red'}]
    // };
    // const keyframes: AnimationKeyframe[] = [
    //   {
    //     offset: 1,
    //     styles: {
    //       styles: [{'stroke': 'purple'}]
    //     }
    //   }
    // ];
    // this.renderer.animate(this.host, startingStyles, keyframes, 5, 0, 'ease-in-out');
  }

}
