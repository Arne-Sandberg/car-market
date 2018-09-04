import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {APIService} from "./api.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  url: string = 'http://127.0.0.1:8000/api/v1/logout';

  constructor(private  apiService: APIService) {
  }


  public logout() {
    this.apiService.logout().subscribe((response) => {
      console.log(response);
    });
  }
}
