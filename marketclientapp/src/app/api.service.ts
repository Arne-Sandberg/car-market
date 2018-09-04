import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class APIService {
  api_url = 'http://127.0.0.1:8000/api/v1/';

  constructor(private  httpClient: HttpClient) {
  }

  getList(list) {
    return this.httpClient.get(`${this.api_url}${list}/`);
  }

  getItem(list, item_id) {
    return this.httpClient.get(`${this.api_url}${list}/${item_id}/`);
  }

  register(data) {
    return this.httpClient.post(`${this.api_url}register/`, data);
  }

  login(data) {
    return this.httpClient.post(`${this.api_url}login/`, data);
  }

  logout() {
    return this.httpClient.post(`${this.api_url}logout/`, null);
  }
}
