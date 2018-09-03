import {Component} from '@angular/core';
import {Http} from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  url: string = 'http://127.0.0.1:8000/api/v1/logout';


  constructor(private http: Http) {
  }


  public logout() {
    this.http.post(this.url, null).toPromise().then((res) => {
      console.log(res);
    });
  }
}
