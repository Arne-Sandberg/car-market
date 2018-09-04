import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/login/';

  constructor() {
  }

  ngOnInit() {
  }

  // data_arr = {
  //   'username': username,
  //   'password': password
  // };

}
