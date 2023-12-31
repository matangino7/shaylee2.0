import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CalendarComponent } from './calendar/calendar.component';
import { GetShiftsComponent } from './get-shifts/get-shifts.component';
import { LoginformComponent } from './loginform/loginform.component';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginpageComponent } from './loginpage/loginpage.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { BroadcastPageComponent } from './broadcast-page/broadcast-page.component';
import { CreateuserComponent } from './createuser/createuser.component';
import { NavbarComponent } from './navbar/navbar.component';
import { MatToolbarModule } from '@angular/material/toolbar'
import { MatButtonModule } from '@angular/material/button'
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
    { path: '', component: LoginpageComponent},
    { path: 'create-user', component: CreateuserComponent },
    { path: 'calendar', component: CalendarComponent },
    { path: 'broadcast', component: BroadcastPageComponent },
    // Add more routes as needed
  ];

@NgModule({
  declarations: [
    AppComponent,
    CalendarComponent,
    GetShiftsComponent,
    LoginformComponent,
    LoginpageComponent,
    BroadcastComponent,
    BroadcastPageComponent,
    CreateuserComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatToolbarModule,
    MatButtonModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent],
  exports: [RouterModule]
})
export class AppModule { }
