import { TestBed } from '@angular/core/testing';

import { GetShiftsService } from './get-shifts.service';

describe('GetShiftsService', () => {
  let service: GetShiftsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetShiftsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
