import { Directive, Renderer, OnInit, Input, HostBinding } from '@angular/core';

@Directive({
  selector: 'path[jlmAnimatedPath]'
})
export class AnimatedPathDirective implements OnInit {
  @Input('jlmAnimatedPath')
  @HostBinding('attr.d')
  jlmAnimatedPath: string;

  constructor(private renderer: Renderer) { }

  ngOnInit() {
  }

}
