import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/login/';
  error: object;

  constructor(private apiService: ApiService,
              private router: Router) {
  }

  ngOnInit() {
  }

  public login(data): void {
    this.apiService.login(data).subscribe((response) => {
      console.log(response);
      if (response)
        this.router.navigateByUrl('/profile');
      else
        this.error = this.apiService.log.pop();
    });
  };
}
