import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  info: object;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getMe()
  }

  public getMe(): void {
    this.apiService.getMe().subscribe((response: object) => {
      console.log(response);
      this.info = response;
    });
  }
}

