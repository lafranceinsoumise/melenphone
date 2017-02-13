/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { PokechonCardComponent } from './pokechon-card.component';

describe('PokechonCardComponent', () => {
  let component: PokechonCardComponent;
  let fixture: ComponentFixture<PokechonCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PokechonCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PokechonCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
