import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetShiftsService {

  constructor(private http: HttpClient) { }

  getShifts(): Observable<any> {
    return this.http.get<any>('http://localhost:8000/api/calendar/', {});
  }
}
