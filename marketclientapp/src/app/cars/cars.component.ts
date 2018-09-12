import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent implements OnInit {
  cars: Array<object>;
  carKeys: Array<string>;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getCars();
  }

  public getImageArray(obj): Array<string> {
    let res: Array<string> = [];
    for (let img of obj['image_set'])
      res.push(img['image']);
    return res;
  }

  public getCars(): void {
    this.apiService.getList('cars').subscribe((response: Array<object>) => {
      console.log(response);
      if (response) {
        this.cars = response;
        this.carKeys = Object.keys(this.cars[0])
          .filter(key => !['id', 'image_set', 'comment_set'].includes(key));
      }
    });
  }
}
