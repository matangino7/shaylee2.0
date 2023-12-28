import { Component, OnInit } from '@angular/core';
import { GetShiftsService } from '../get-shifts.service';


interface Shift {
  a_post?: {
    first_guard?: string;
    second_guard?: string;
  };
  b_post?: {
    first_guard?: string;
    second_guard?: string;
  };
  manning_post?: {
    first_guard?: string;
    second_guard?: string;
  }
}


@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})
export class CalendarComponent implements OnInit {

  constructor(private getShiftsService: GetShiftsService) {}

  public calendarData: any[][] = [];
  public weekHebrew: string[] = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת'];
  public shiftData: { [day: number]: Shift } = {};

  ngOnInit(): void {
    this.renderCalendar();
  }

  renderCalendar(): void {
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
  
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);
  
    const daysOfWeek: string[] = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  
    // Determine the starting day for the first week
    const startDay = (firstDayOfMonth.getDay() - daysOfWeek.indexOf('Sun') + 7) % 7;
  
    // Create calendar days
    let currentRow: any[] = [];
  
    for (let i = 0; i < startDay; i++) {
      currentRow.push(null); // Use null for empty cells
    }
  
    for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
      const date = new Date(currentYear, currentMonth, day);
      currentRow.push({
        day: day,
        isCurrentDay: date.toDateString() === now.toDateString()
      });
  
      if ((startDay + day - 1) % 7 === 6 || day === lastDayOfMonth.getDate()) {
        this.calendarData.push(currentRow);
        currentRow = [];
      }
    }
      if (this.calendarData.length > 0) {
      this.calendarData.unshift(daysOfWeek);
    }
  }
  
  getShiftData(): void {
    this.getShiftsService.getShifts()
      .subscribe(data => {
        this.handleShiftsFetched(data);
      });
  }

  handleShiftsFetched(data: any): void {
    this.shiftData = data;
  }  


}
