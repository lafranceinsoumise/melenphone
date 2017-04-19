import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';

import { RootState, getWebsocket } from '../rx/reducers';
import * as fromWebsocket from '../rx/reducers/websocket.reducer';

import {
  CreateNewConnectionAction,
  OpenEventAction,
  MessageEventAction,
  ErrorEventAction,
  CloseEventAction
} from '../rx/actions/websocket.actions';

type WebsocketScheme = 'wss' | 'ws';

@Injectable()
export class SocketConnectionService {
  scheme: WebsocketScheme = (window.location.protocol === 'https:') ? 'wss' : 'ws';
  room: WebSocket;
  url = `${this.scheme}://${window.location.hostname}:${window.location.port}/websocket`;

  constructor(private store: Store<RootState>) {
    this.store.select(getWebsocket)
      .subscribe((value: fromWebsocket.State) => {
        this.room = value.currentWebSocket;
      });
  }

  start() {
    this.store.dispatch(new CreateNewConnectionAction(new WebSocket(this.url)));
  }

  start2() {
    this.room = new WebSocket(this.url);
    this.store.dispatch(new CreateNewConnectionAction(this.room));
    this.room.addEventListener('open', (event: Event) => {
      this.store.dispatch(new OpenEventAction());
    });
    this.room.addEventListener('message', (event: MessageEvent) => {
      const parsed = JSON.parse(event.data);
      this.store.dispatch(new MessageEventAction(parsed));
    });
    this.room.addEventListener('error', (event: MessageEvent) => {
      const parsed = JSON.parse(event.data);
      this.store.dispatch(new ErrorEventAction(parsed));
    });
    this.room.addEventListener('close', (event: MessageEvent) => {
      const parsed = JSON.parse(event.data);
      this.store.dispatch(new CloseEventAction(parsed));
    });
  }

}
