import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-item',
  templateUrl: './item.component.html',
  styleUrls: ['./item.component.css']
})
export class ItemComponent implements OnInit {
  item: object = null;
  ids: Array<number> = [];
  item_keys: Array<string> = [];
  list_names: Array<string> = ['cars', 'users', 'comments'];

  constructor(private  apiService: ApiService) {
  }

  ngOnInit() {
    this.getIds(this.list_names[0]);
  }

  public getIds(list_name) {
    this.apiService.getList(list_name).subscribe((data: Array<object>) => {
      this.ids = [];
      for (let i of data) {
        this.ids.push(i['id']);
      }
      console.log(data);
    });
  }

  public getItem(list_name, item_id) {
    if (this.ids.length) {
      this.apiService.getItem(list_name, item_id).subscribe((response: object) => {
        this.item = response;
        this.item_keys = Object.keys(this.item);
        console.log(response);
      });
    }
    else {
      this.item = null;
      this.item_keys = [];
    }
  }
}
