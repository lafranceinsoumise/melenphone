import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'jlm-gauge',
  templateUrl: './gauge.component.html',
  styleUrls: ['./gauge.component.scss']
})
export class GaugeComponent implements OnInit {

  @Input() min = 1;
  @Input() max = 10;
  @Input() value = 0;

  constructor() { }

  ngOnInit() {
  }

}
