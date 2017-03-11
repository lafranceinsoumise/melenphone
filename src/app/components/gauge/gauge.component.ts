import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'jlm-gauge',
  templateUrl: './gauge.component.html',
  styleUrls: ['./gauge.component.scss']
})
export class GaugeComponent implements OnInit {

  @Input() min = 100;
  @Input() max = 1000;
  @Input() value = null;

  constructor() { }

  ngOnInit() {
  }

}
