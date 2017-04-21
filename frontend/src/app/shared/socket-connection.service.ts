import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs/Observable';

import { RootState, getWebsocket } from '../rx/reducers';
import * as fromWebsocket from '../rx/reducers/websocket.reducer';

import {
  CreateNewConnectionAction,
  OpenEventAction,
  MessageEventAction,
  ErrorEventAction,
  CloseEventAction
} from '../rx/actions/websocket.actions';

@Injectable()
export class SocketConnectionService {
  room: WebSocket;
  open$: Observable<Event>;
  message$: Observable<MessageEvent>;
  error$: Observable<MessageEvent>;
  close$: Observable<Event>;

  constructor(private store: Store<RootState>) {
    this.store.select(getWebsocket)
      .subscribe((value: fromWebsocket.State) => {
        console.info(`I'm subscribing to a new Websocket`);
        if (value.currentWebSocket === null) return;
        this.room = value.currentWebSocket;
        this.addWebsocketListeners(this.room);
      });
  }

  // start() {
  //   this.store.dispatch(new CreateNewConnectionAction(new WebSocket(this.url)));
  // }

  addWebsocketListeners(socket: WebSocket) {
    this.open$ = Observable.fromEvent(socket, 'open');
    this.message$ = Observable.fromEvent(socket, 'message');
    this.error$ = Observable.fromEvent(socket, 'error');
    this.close$ = Observable.fromEvent(socket, 'close');

    // this.message$.subscribe(val => {
    //   const parsed = JSON.parse(val.data);
    //   switch(parsed.type) {
    //     case ''
    //   }
    // });
    // this.room.addEventListener('open', (event: Event) => {
    //   this.store.dispatch(new OpenEventAction());
    // });
    // this.room.addEventListener('message', (event: MessageEvent) => {
    //   const parsed = JSON.parse(event.data);
    //   this.store.dispatch(new MessageEventAction(parsed));
    // });
    // this.room.addEventListener('error', (event: MessageEvent) => {
    //   const parsed = JSON.parse(event.data);
    //   this.store.dispatch(new ErrorEventAction(parsed));
    // });
    // this.room.addEventListener('close', (event: MessageEvent) => {
    //   const parsed = JSON.parse(event.data);
    //   this.store.dispatch(new CloseEventAction(parsed));
    // });
  }

}
