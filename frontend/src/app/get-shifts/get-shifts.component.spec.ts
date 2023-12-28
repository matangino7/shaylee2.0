import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetShiftsComponent } from './get-shifts.component';

describe('GetShiftsComponent', () => {
  let component: GetShiftsComponent;
  let fixture: ComponentFixture<GetShiftsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GetShiftsComponent]
    });
    fixture = TestBed.createComponent(GetShiftsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
