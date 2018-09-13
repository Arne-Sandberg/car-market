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
import {CarsComponent} from './cars/cars.component';
import {HomeComponent} from './home/home.component';
import {LoginModalComponent} from './login-modal/login-modal.component';
import {RegisterModalComponent} from './register-modal/register-modal.component';
import {EditCommentModalComponent} from './edit-comment-modal/edit-comment-modal.component';
import {EditProfileModalComponent } from './edit-profile-modal/edit-profile-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    UserComponent,
    CarComponent,
    CreateComponent,
    CarsComponent,
    HomeComponent,
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    NgbModule.forRoot(),
  ],
  exports: [
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
  ],
  entryComponents: [
    LoginModalComponent,
    RegisterModalComponent,
    EditCommentModalComponent,
    EditProfileModalComponent,
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
