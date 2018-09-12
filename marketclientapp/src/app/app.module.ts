import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from "@angular/forms";
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {UserComponent} from './user/user.component';
import {CarComponent} from './car/car.component';
import {CreateComponent} from './create/create.component';
import {ApiService} from "./api.service";
import {ProfileComponent} from './profile/profile.component';
import {CarsComponent} from './cars/cars.component';
import {HomeComponent} from './home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    UserComponent,
    CarComponent,
    CreateComponent,
    ProfileComponent,
    CarsComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    NgbModule.forRoot(),
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
