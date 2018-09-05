import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/login/';

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
  }

  onSubmit(){

  }
  public login(data) {
    this.apiService.login(data).subscribe((response) => {
      console.log(response);
    });
  };
}
