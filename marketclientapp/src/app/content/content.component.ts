import {Component, OnInit} from '@angular/core';
import {Http} from "@angular/http";

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/';
  pk: number;
  single: boolean;
  response;
  keys;

  constructor(private http: Http) {
  }

  ngOnInit() {
  }

  public getMultipleInfo(flag) {
    this.http.get(this.url + flag).toPromise().then((res) => {
      console.log(res);
      this.response = res.json();
      this.single = false;
      console.log(this.single);
      this.keys = this.response ? Object.keys(this.response[0]) : null;
    });
  }

  public getSingleInfo(flag) {
    this.http.get(this.url + flag + '/' + this.pk).toPromise().then((res) => {
      console.log(res);
      this.response = res.json();
      this.single = true;
      console.log(this.single);
      this.keys = this.response ? Object.keys(this.response) : null;
    });
  }

  public makePk(event: any) {
    this.pk = event.target.value;
  }

}
