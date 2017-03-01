import { Directive, Input, Output, HostListener, ElementRef } from '@angular/core';

import { FullscreenService } from './fullscreen.service';

@Directive({
  selector: '[jlmFullscreen]',
  exportAs: 'fullscreen'
})
export class FullscreenDirective {
  elementIsFullscreen = false;

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
    if ('requestFullscreen' in this.elRef.nativeElement) {
      this.elRef.nativeElement.requestFullscreen();
    } else if ('mozRequestFullScreen' in this.elRef.nativeElement) {
      this.elRef.nativeElement.mozRequestFullScreen();
    } else if ('msRequestFullscreen' in this.elRef.nativeElement) {
      this.elRef.nativeElement.msRequestFullscreen();
    } else if ('webkitRequestFullscreen' in this.elRef.nativeElement) {
      this.elRef.nativeElement.webkitRequestFullscreen();
    } else {
      console.error('your navigator does not support fullscreen mode');
    }
  }

  exitFullscreen() {
    this.fs.exitFullscreen();
  }

}
