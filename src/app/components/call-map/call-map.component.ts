import { Component, OnInit, ViewContainerRef, ViewRef, ViewChild, Renderer, ElementRef } from '@angular/core';
import {
  trigger,
  state,
  style,
  transition,
  animate } from '@angular/core';
import { SocketConnectionService, CoordinatesConverterService } from '../../shared';
import { WsCallNotification } from '../../core';

@Component({
  selector: 'jlm-call-map',
  templateUrl: './call-map.component.html',
  styleUrls: ['./call-map.component.scss'],
  animations: [
    trigger('heroState', [
      state('inactive', style({
        backgroundColor: 'forestgreen'
      })),
      state('active', style({
        backgroundColor: 'firebrick'
      })),
      transition('active => inactive', animate('100ms ease-in')),
      transition('inactive => active', animate('100ms ease-out'))
    ])
  ]
})
export class CallMapComponent implements OnInit {
  @ViewChild('mypath', {read: ViewContainerRef}) mypath: ViewContainerRef;
  @ViewChild('svgDocument') svgRef: ElementRef;
  paths: any[] = [
    {d: `M790.5,316.2l6.7-20.5l0.4,1.1l1.4-0.8l3,1.8l3.3-1.5l1.3,0.3l0-0.9l1.6,0.8l1.2,2.9l3.3,0.7l0,0
		l0.4,1.1l-1,0.9l3.2,1.9l-0.6,0.7l1.7,1.9l0,1.7l0.8-2.2l0.5,2l1.6,0l-0.8,2.5l0.7,0.6l2.7-0.3l1.1-1.6l1.2-0.1l2-2.9l0.1,1.2
		l2.8,0.9l0.5,2.9l6-0.2l8.1-9.1l0,0l4.4,2.9l-2.8,4.9l0.9,2l-6,2.1l-0.6,1.2l1.3,0.9l-1.6,2.9l0,0l-2.6,0.8l-0.3,2l-2.8-1.1
		l-0.6,5.3l1.2,2.5l-0.2,2.1l0,0l-2.2,12.7l-1.1,1.1l-2-0.3l-0.6,4.1l-2.6,1.7l0,0l-1-2.7l-2.4-2l0.4-1l-5.4-5.7l0.3-1.8l-3.3-2.8
		l-2.1,2.1l-1.3,3.3l-1.9,1.4l-1.4-0.2l-1.6-2l-1.4-0.3l-0.3,0.8l-0.2-0.9l0,0l-7.6,0.6v-2.3l-1.5-3.3l-1.4-1l-1.8,1l0.2-1.4
		l-3.3-1.3l1-1.8l-0.3-7l2.3-3.7L790.5,316.2z`}
  ];
  length = 0;
  notifications: WsCallNotification[] = [];

  constructor(
    private renderer: Renderer,
    private scs: SocketConnectionService,
    private coordsCvrtr: CoordinatesConverterService) {}

  ngOnInit() {
    const svgCoords = this.coordsCvrtr.getSvgLocation(48.577725, 7.738060);
    console.assert(svgCoords[0] === 0.6690940204559985, 'wrong conversion');
    console.assert(svgCoords[1] === 0.2139674699484885, 'wrong conversion');
    this.scs.room.addEventListener('message', (event) => this.onCallNotification(event), false);
  }

  getSvgDimensions(): {width: number, height: number} {
    const natel = this.svgRef;
    console.log(natel);
    // this.renderer.
    return {width: 1366, height: 768};
  }

  onCallNotification(event: MessageEvent) {
    const call: WsCallNotification = JSON.parse(event.data);
    const callerSvgCoords = this.coordsCvrtr.getSvgLocation(call.caller.gps.lat, call.caller.gps.lng);
    const calleeSvgCoords = this.coordsCvrtr.getSvgLocation(call.callee.gps.lat, call.callee.gps.lng);
    const {width: mapWidth, height: mapHeight} = this.getSvgDimensions();
    call.caller.svg = {x: callerSvgCoords[0] * mapWidth, y: callerSvgCoords[1] * mapHeight};
    call.callee.svg = {x: calleeSvgCoords[0] * mapWidth, y: calleeSvgCoords[1] * mapHeight};
    this.notifications.push(call);
  }

}
