import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'jlm-dynamic-component',
  template: `
  yeah dyn works
  `,
  styleUrls: ['./dynamic-component.component.scss']
})
export class DynamicComponentComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
