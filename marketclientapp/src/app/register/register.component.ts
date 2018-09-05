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

  public register(data) {
    let data_dict = {
      'username': data.username,
      'email': data.email,
      'password1': data.password1,
      'password2': data.password2,
    };
    this.apiService.register(data_dict).subscribe((response) => {
      console.log(response);
    });
  };

}
