import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {UserComponent} from "./user/user.component";
import {CarComponent} from "./car/car.component";
import {CreateComponent} from "./create/create.component";
import {ProfileComponent} from "./profile/profile.component";
import {CarsComponent} from "./cars/cars.component";
import {HomeComponent} from "./home/home.component";

const routes: Routes = [
  {path: 'users/:id', component: UserComponent},
  {path: 'cars', component: CarsComponent},
  {path: 'cars/:id', component: CarComponent},
  {path: 'create', component: CreateComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'home', component: HomeComponent},
  {path: '', redirectTo: '/home', pathMatch: 'full'},
];

@NgModule({
  exports: [RouterModule],
  imports: [RouterModule.forRoot(routes)],
})
export class AppRoutingModule {
}

