import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent implements OnInit {
  cars: Array<any>;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getCars();
  }

  private getCars(): void {
    this.apiService.getList('cars').subscribe((response: Array<object>) => {
      console.log(response);
      if (response) {
        this.cars = response;
        for (let car of this.cars)
          car.brand = this.apiService.brands.find(brand => brand.id == car.brand).name;
      }
    });
  }
}
