import {Component, OnInit} from '@angular/core';
import {APIService} from "../api.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/login/';

  constructor(private apiService: APIService) {
  }

  ngOnInit() {
  }


  public login(username, password) {
    let data = {
      'username': username,
      'password': password,
    };
    this.apiService.login(data).subscribe((response) => {
      console.log(response);
    });
  };
}
