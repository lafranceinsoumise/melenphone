import { Injectable } from '@angular/core';

@Injectable()
export class FullscreenService {

  constructor() { }

  get exitFullscreen() {
    let exitFn = document.exitFullscreen || document.webkitExitFullscreen;
    if ('mozCancelFullScreen' in document) {
      exitFn = document['mozCancelFullScreen'];
    } else if ('msExitFullscreen' in document) {
      exitFn = document['msExitFullscreen'];
    }
    return exitFn.bind(document);
  }

}
