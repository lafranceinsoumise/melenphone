import {
  Component,
  Input,
  OnInit,
  OnDestroy,
  AfterViewInit,
  ViewContainerRef,
  ViewRef,
  ViewChild,
  ElementRef
} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';
import { Store } from '@ngrx/store';

import {
  SocketConnectionService,
  CoordinatesConverterService,
  MapService,
  CallLocationDescription,
  WebSocketCallMessage
} from '../../shared';

import { RootState, getCallsState } from '../../rx/reducers';
import * as fromCall from '../../rx/reducers/call.reducer';

@Component({
  selector: 'jlm-call-map',
  templateUrl: './call-map.component.html',
  styleUrls: ['./call-map.component.scss']
})
export class CallMapComponent implements OnInit, OnDestroy, AfterViewInit {
  newCall$: Observable<fromCall.State>;
  newCall$Subscription: Subscription;
  displayedCalls$: Observable<WebSocketCallMessage[]>;

  @ViewChild('svgDocument') svgRef: ElementRef;
  notifications: { call: CallLocationDescription, options: any}[] = [];
  shouldAnimate = false;

  @Input() timeout = 3000;

  constructor(
    private scs: SocketConnectionService,
    private mapService: MapService,
    private rootStore: Store<RootState>,
    private coordsCvrtr: CoordinatesConverterService) {}

  ngOnInit() {
    this.newCall$ = this.rootStore.select(getCallsState);
    this.shouldAnimate = this.mapService.firstTime;
    this.newCall$Subscription = this.newCall$.subscribe((state: fromCall.State) => {
      if (!state.lastCall) return;
      this.pushCall(state.lastCall);
    });
  }

  ngOnDestroy() {
    this.newCall$Subscription.unsubscribe();
  }

  ngAfterViewInit() {
      this.mapService.firstTime = false;
  }

  getSvgDimensions(): {width: number, height: number} {
    const natel = this.svgRef;
    return {width: 1366, height: 768};
  }

  pushCall(rawNotification: WebSocketCallMessage) {
    const call: CallLocationDescription = {
      caller: {
        gps: {
            lat: +rawNotification.call.caller.lat,
            lng: +rawNotification.call.caller.lng
        }
      },
      callee: {
          gps: {
            lat: +rawNotification.call.target.lat,
            lng: +rawNotification.call.target.lng
          }
      }
    };
    const callerSvgCoords = this.coordsCvrtr.getSvgLocation(call.caller.gps.lat, call.caller.gps.lng);
    const calleeSvgCoords = this.coordsCvrtr.getSvgLocation(call.callee.gps.lat, call.callee.gps.lng);
    const {width: mapWidth, height: mapHeight} = this.getSvgDimensions();
    call.caller.svg = {x: callerSvgCoords.x * mapWidth, y: callerSvgCoords.y * mapHeight};
    call.callee.svg = {x: calleeSvgCoords.x * mapWidth, y: calleeSvgCoords.y * mapHeight};
    const notifRef = {call, options: {removeStart: false}};
    this.notifications.push(notifRef);
    setTimeout(
      () => {
        notifRef.options.removeStart = true;
        setTimeout(() => this.notifications.splice(this.notifications.indexOf(notifRef), 1), 1100);
      }, this.timeout);
  }

}
