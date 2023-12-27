import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-broadcast',
  templateUrl: './broadcast.component.html',
  styleUrls: ['./broadcast.component.css']
})
export class BroadcastComponent implements OnInit{
    loginForm!: FormGroup;

  constructor(private fb: FormBuilder, private http: HttpClient) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      message: ['', [Validators.required]]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const data = this.loginForm.value;
      const apiEndpoint = 'http://127.0.0.1:5020/broadcast';
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
      });
  
      const jsonData = JSON.stringify(data);
      console.log(jsonData)
  
      this.http.post(apiEndpoint, jsonData, { headers }).subscribe(
        (response) => {
          console.log('Success:', response);
        },
        (error) => {
          console.error('Error:', error);
        }
      );
    }
  }
}
