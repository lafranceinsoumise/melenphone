/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { RiriComponent } from './riri.component';

describe('RiriComponent', () => {
  let component: RiriComponent;
  let fixture: ComponentFixture<RiriComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RiriComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RiriComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
