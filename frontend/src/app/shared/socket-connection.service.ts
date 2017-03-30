import { Injectable } from '@angular/core';

type WebsocketScheme = 'wss' | 'ws';

@Injectable()
export class SocketConnectionService {
  scheme: WebsocketScheme;
  room: WebSocket;

  constructor() {
    this.scheme = (window.location.protocol === 'https:') ? 'wss' : 'ws';
    const wsUrl = `${this.scheme}://${window.location.hostname}:${window.location.port}/websocket`;
    this.room = new WebSocket(wsUrl);
  }

}
