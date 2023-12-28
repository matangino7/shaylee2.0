import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-createuser',
  templateUrl: './createuser.component.html',
  styleUrls: ['./createuser.component.css']
})
export class CreateuserComponent implements OnInit{
    loginForm!: FormGroup;

    constructor(private fb: FormBuilder, private http: HttpClient) {}
  
    ngOnInit() {
      this.loginForm = this.fb.group({
        id: ['', [Validators.required]],
        first_name: ['', Validators.required],
        last_name: ['', Validators.required],
        birth_date: ['', Validators.required],
        phone_number: ['', Validators.required],
        commander_contact: ['', Validators.required],
        b_objection: ['False', Validators.required],
        lieutenant: ['False', Validators.required],
      });
    }
  
    onSubmit() {
        console.log(this.loginForm.valid)
      if (this.loginForm.value) {
        const data = this.loginForm.value;
        const apiEndpoint = 'http://127.0.0.1:8000/api/api/users/';
  
        this.http.post(apiEndpoint, data).subscribe(
          (response) => {
            console.log('Success:', response);
            var pass = (response as any).password
            alert(`the password is ${pass}`);
          },
          (error) => {
            console.error('Error:', error);
          }
        );
      }
    }
}
