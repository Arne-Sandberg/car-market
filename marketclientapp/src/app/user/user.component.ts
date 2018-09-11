import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  @Input() id: string;
  info: object;
  image: string;
  cars: Array<object>;
  purchases: Array<object>;
  infoKeys: Array<string>;
  error: object;

  constructor(private apiService: ApiService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.getUser(this.id);
  }

  public getUser(id): void {
    if (!id)
      id = this.route.snapshot.paramMap.get('id');
    this.apiService.getItem('users', id).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.info = response;
        this.image = this.info['image'];
        this.purchases = [];
        for (let purchase of this.info['purchase_set'])
          this.apiService.getItem('cars', purchase['car']).subscribe((response: object) => {
            purchase['car'] = response;
            this.purchases.push(purchase);
          });
        this.cars = [];
        for (let car of this.info['car_set'])
          this.apiService.getItem('cars', car).subscribe((response: object) => {
            this.cars.push(response);
          });
        this.infoKeys = Object.keys(this.info).filter(
          key => !['image', 'id', 'car_set', 'purchase_set',].includes(key));
      }
      else
        this.error = this.apiService.log.pop();
    });
  }
}
