import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';


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


@NgModule({
  declarations: [
    AppComponent,
    CalendarComponent,
    GetShiftsComponent,
    LoginformComponent,
    LoginpageComponent,
    BroadcastComponent,
    BroadcastPageComponent,
    CreateuserComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
