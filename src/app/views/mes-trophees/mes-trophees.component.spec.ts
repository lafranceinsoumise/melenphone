import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MesTropheesComponent } from './mes-trophees.component';

describe('MesTropheesComponent', () => {
  let component: MesTropheesComponent;
  let fixture: ComponentFixture<MesTropheesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MesTropheesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MesTropheesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
