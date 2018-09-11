import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {RegisterComponent} from "./register/register.component";
import {UserComponent} from "./user/user.component";
import {CarComponent} from "./car/car.component";
import {CreateComponent} from "./create/create.component";
import {ProfileComponent} from "./profile/profile.component";
import {CarsComponent} from "./cars/cars.component";

const routes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'users/:id', component: UserComponent},
  {path: 'cars', component: CarsComponent},
  {path: 'cars/:id', component: CarComponent},
  {path: 'create', component: CreateComponent},
  {path: 'profile', component: ProfileComponent},
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)],
})
export class AppRoutingModule {
}

