import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class APIService {
  API_URL = 'http://127.0.0.1:8000/api/v1/';

  constructor(private  httpClient: HttpClient) {
  }

  getList(list) {
    return this.httpClient.get(`${this.API_URL}${list}/`);
  }

  registerUser(data) {
    return this.httpClient.post(`${this.API_URL}register/`, data);
  }

  logout() {
    return this.httpClient.post(`${this.API_URL}logout/`, null);
  }
}
