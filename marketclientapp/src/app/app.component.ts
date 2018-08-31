import {Component} from '@angular/core';
import {Http, Response} from '@angular/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Car market';
  url: string = 'http://127.0.0.1:8000/api/v1/';
  multinfo;
  singleinfo;
  pk;

  constructor(private http: Http) {
  }

  public getMultipleInfo(flag) {
    this.http.get(this.url + flag).toPromise().then((res) => {
      this.multinfo = res.json();
    });
  }

  public getSingleInfo(flag) {
    this.http.get(this.url + flag + '/' + this.pk + '/').toPromise().then((res) => {
      this.singleinfo = res.json();
    });
  }

  public makePk(event: any) {
    this.pk = event.target.value;
  }

  public register(username, email, password1, password2) {
    let data = {
      'username': username,
      'email':email,
      'password1': password1,
      'password2': password2,
    };
    console.log(data);
    this.http.post(this.url + 'register/', data).toPromise().then((res) => {
      console.log(res);
      this.singleinfo = res.json();
    });
  }

  public login(username, password) {
    let data_arr = {'username': username, 'password': password};
    this.http.post(this.url + 'login/', data_arr).toPromise().then((res) => {
      console.log(res);
      this.singleinfo = res.json();
    });
  }

  public logout() {
    this.http.post(this.url + 'logout/', null).toPromise().then((res) => {
      console.log(res);
      this.singleinfo = res.json();
    });
  }
}
