import {Component, OnInit} from '@angular/core';
import {Http} from '@angular/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/register/';

  constructor(private http: Http) {
  }

  ngOnInit() {
  }

  public register(username, email, password1, password2) {
    let data = {
      'username': username,
      'email': email,
      'password1': password1,
      'password2': password2,
    };
    this.http.post(this.url, data).toPromise().then((res) => {
      console.log(res);
    });

  }
}
