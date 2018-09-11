import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent implements OnInit {
  list: Array<object>;
  list_keys: Array<string>;
  title: string = 'cars';

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getList(this.title);
  }

  public getImageArray(obj): Array<string> {
    let res: Array<string> = [];
    for (let img of obj['image_set'])
      res.push(img['image']);
    return res;
  }

  public getList(list_name): void {
    this.apiService.getList(list_name).subscribe((response: Array<object>) => {
      console.log(response);
      this.list = response;
      this.list_keys = this.list.length ? Object.keys(this.list[0]).filter(
        key => !['id', 'image_set', 'comment_set'].includes(key)) : [];
    });
  }
}
