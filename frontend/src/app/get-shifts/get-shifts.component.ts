// get-shifts.component.ts

import { Component, Output, EventEmitter } from '@angular/core';
import { GetShiftsService } from '../get-shifts.service';

@Component({
  selector: 'app-get-shifts',
  templateUrl: './get-shifts.component.html',
  styleUrls: ['./get-shifts.component.css']
})
export class GetShiftsComponent {
  @Output() shiftsFetched = new EventEmitter<any>();

  constructor(private getShiftsService: GetShiftsService) {}

  getShifts(): void {
    this.getShiftsService.getShifts()
      .subscribe(data => {
        this.shiftsFetched.emit(data);
      });
  }
}