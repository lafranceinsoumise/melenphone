/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { LoulouComponent } from './loulou.component';

describe('LoulouComponent', () => {
  let component: LoulouComponent;
  let fixture: ComponentFixture<LoulouComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoulouComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoulouComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
