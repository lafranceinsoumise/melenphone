import { Injectable } from '@angular/core';

type WebsocketScheme = 'wss' | 'ws';

@Injectable()
export class SocketConnectionService {
  scheme: WebsocketScheme;
  room: WebSocket;

  constructor() {
    this.scheme = (window.location.protocol === 'https:') ? 'wss' : 'ws';
    const wsUrl = `${this.scheme}://${window.location.hostname}:${8000}`;
    this.room = new WebSocket(wsUrl);
  }

}
