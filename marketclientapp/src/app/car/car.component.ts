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
  item_keys: Array<string>;
  comments: Array<object>;

  constructor(private apiService: ApiService,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.getItem();
  }

  public getItem(): void {
    this.apiService.getItem('cars', this.route.snapshot.paramMap.get('id')).subscribe((response: object) => {
      console.log(response);
      this.car = response;
      if (this.car) {
        this.item_keys = Object.keys(this.car).filter(key => !['id', 'image_set', 'comment_set'].includes(key));
        this.comments = this.car['comment_set'];
      }
    });
  }
}
