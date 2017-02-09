/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { CodexComponent } from './codex.component';

describe('CodexComponent', () => {
  let component: CodexComponent;
  let fixture: ComponentFixture<CodexComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CodexComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CodexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
