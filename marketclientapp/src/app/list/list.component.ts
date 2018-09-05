import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-car-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {
  list: Array<object> = [];
  list_keys: Array<string> = [];
  list_names: Array<string> = ['cars', 'users', 'comments', 'adds'];

  constructor(private  apiService: ApiService) {
  }

  ngOnInit() {
  }

  public getList(list_name) {
    this.apiService.getList(list_name).subscribe((response: Array<object>) => {
      this.list = response;
      this.list_keys = this.list.length ? Object.keys(this.list[0]) : [];
      console.log(response);
    });
  }
}
