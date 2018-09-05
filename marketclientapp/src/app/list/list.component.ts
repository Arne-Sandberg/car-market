import {Component, OnInit} from '@angular/core';
import {APIService} from '../api.service';

@Component({
  selector: 'app-car-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {
  list: Array<object> = [];
  list_keys: Array<string> = [];
  list_names: Array<string> = ['cars', 'users', 'comments', 'adds'];

  constructor(private  apiService: APIService) {
  }

  ngOnInit() {
  }

  public getList(list_name) {
    this.apiService.getList(list_name).subscribe((data: Array<object>) => {
      this.list = data;
      this.list_keys = this.list.length ? Object.keys(this.list[0]) : [];
      console.log(data);
    });
  }
}
