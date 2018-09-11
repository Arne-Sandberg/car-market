import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from "@angular/forms";

import {AppComponent} from './app.component';
import {RegisterComponent} from './register/register.component';
import {LoginComponent} from './login/login.component';
import {AppRoutingModule} from './app-routing.module';
import {UserComponent} from './user/user.component';
import {CarComponent} from './car/car.component';
import {CreateComponent} from './create/create.component';
import {ApiService} from "./api.service";
import {ProfileComponent} from './profile/profile.component';
import {CarsComponent} from './cars/cars.component';
import {SlideshowModule} from 'ng-simple-slideshow';

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    LoginComponent,
    UserComponent,
    CarComponent,
    CreateComponent,
    ProfileComponent,
    CarsComponent,
  ],
  imports: [
    SlideshowModule,
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
