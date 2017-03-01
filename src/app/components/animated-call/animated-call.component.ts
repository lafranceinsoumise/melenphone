import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'jlm-animated-call',
  template: `
    <svg:path></path>
  `,
  styles: []
})
export class AnimatedCallComponent implements OnInit {
  @Input()
  description: string;

  constructor() { }

  ngOnInit() {
  }

}
