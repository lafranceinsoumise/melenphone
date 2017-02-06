/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { FifiComponent } from './fifi.component';

describe('FifiComponent', () => {
  let component: FifiComponent;
  let fixture: ComponentFixture<FifiComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FifiComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FifiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
