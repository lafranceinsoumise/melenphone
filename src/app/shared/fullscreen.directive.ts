import { Directive, Input, Output, HostListener, ElementRef } from '@angular/core';

import { FullscreenService } from './fullscreen.service';

@Directive({
  selector: '[jlmFullscreen]',
  exportAs: 'fullscreen'
})
export class FullscreenDirective {
  elementIsFullscreen: boolean = false;

  constructor(private elRef: ElementRef, private fs: FullscreenService) { }

  toggle(value: boolean) {
    this.elementIsFullscreen = value;
    if (value) {
      this.requestFullscreen();
    }
  }

  get isFullscreen() {
    let fullscreenElement = document.fullscreenElement || document.webkitFullscreenElement;
    // this workaround is due to an error in the typescript compiler
    if ('mozFullScreenElement' in document) {
      fullscreenElement = document['mozFullScreenElement'];
    } else if ('msFullscreenElement' in document) {
      fullscreenElement = document['msFullscreenElement'];
    }
    return this.elRef.nativeElement === fullscreenElement;
  }

  requestFullscreen() {
    this.elRef.nativeElement.webkitRequestFullscreen();
  }

  exitFullscreen() {
    this.fs.exitFullscreen();
  }

}
