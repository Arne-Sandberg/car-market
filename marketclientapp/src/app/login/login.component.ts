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

  onSubmit(){

  }
  public login(data) {
    let data_dict = {
      'username': data.username,
      'password': data.password,
    };
    this.apiService.login(data_dict).subscribe((response) => {
      console.log(response);
    });
  };
}
