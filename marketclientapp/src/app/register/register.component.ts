import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
  }

  public register(data) {
    this.apiService.register(data).subscribe((response) => {
      console.log(response);
    });
  };

}
