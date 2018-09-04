import {Component, OnInit} from '@angular/core';
import {APIService} from '../api.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  constructor(private apiService: APIService) {
  }

  ngOnInit() {
  }

  public registerUser(username, email, password1, password2) {
    let data = {
      'username': username,
      'email': email,
      'password1': password1,
      'password2': password2,
    };
    this.apiService.registerUser(data).subscribe((response) => {
      console.log(response);
    });
  };

}
