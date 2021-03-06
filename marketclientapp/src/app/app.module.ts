import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from "@angular/forms";
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {NgxStripeModule} from 'ngx-stripe';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {UserComponent} from './user/user.component';
import {CarComponent} from './car/car.component';
import {ApiService} from "./api.service";
import {CarsComponent} from './cars/cars.component';
import {HomeComponent} from './home/home.component';
import {LoginModalComponent} from './login-modal/login-modal.component';
import {RegisterModalComponent} from './register-modal/register-modal.component';
import {EditCommentModalComponent} from './edit-comment-modal/edit-comment-modal.component';
import {EditProfileModalComponent} from './edit-profile-modal/edit-profile-modal.component';
import {CheckoutModalComponent} from './checkout-modal/checkout-modal.component';
import {CarModalComponent} from './car-modal/car-modal.component';
import {CheckoutResultModalComponent} from './checkout-result-modal/checkout-result-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    UserComponent,
    CarComponent,
    CarsComponent,
    HomeComponent,
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
    CheckoutModalComponent,
    CarModalComponent,
    CheckoutResultModalComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    NgbModule.forRoot(),
    NgxStripeModule.forRoot('pk_test_0iZ2ciCzQWinzLyvzEzkuWiE'),
  ],
  exports: [
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
    CheckoutModalComponent,
    CarModalComponent,
    CheckoutResultModalComponent,
  ],
  entryComponents: [
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
    CheckoutModalComponent,
    CarModalComponent,
    CheckoutResultModalComponent,
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
