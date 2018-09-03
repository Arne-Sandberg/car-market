import {Component, OnInit} from '@angular/core';
import {Http} from "@angular/http";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/login/';

  constructor(private http: Http) {
  }

  ngOnInit() {
  }

  public login(username, password) {
    let data_arr = {
      'username': username,
      'password': password
    };
    this.http.post(this.url, data_arr).toPromise().then((res) => {
      console.log(res);
    });
  }
}
