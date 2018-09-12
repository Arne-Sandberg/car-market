import {Component, OnInit} from '@angular/core';
import {ApiService} from "./api.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/logout';

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
  }

  public logout(): void {
    this.apiService.logout().subscribe((response) => {
      console.log(response);
    });
  }
}
