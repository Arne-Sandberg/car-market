import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {
  car: object;
  error: object;

  constructor(private apiService: ApiService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.getItem();
  }

  public getItem(): void {
    this.apiService.getItem('cars', this.route.snapshot.paramMap.get('id'))
      .subscribe((response: object) => {
        console.log(response);
        response ? this.car = response : this.error = this.apiService.errorLog.pop();
      });
  }
}
