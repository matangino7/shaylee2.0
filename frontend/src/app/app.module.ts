import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginformComponent } from './loginform/loginform.component';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { LoginpageComponent } from './loginpage/loginpage.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { BroadcastPageComponent } from './broadcast-page/broadcast-page.component';
import { CreateuserComponent } from './createuser/createuser.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginformComponent,
    LoginpageComponent,
    BroadcastComponent,
    BroadcastPageComponent,
    CreateuserComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
