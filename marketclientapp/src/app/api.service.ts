import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class APIService {
  api_url = 'http://127.0.0.1:8000/api/v1/';

  constructor(private  httpClient: HttpClient) {
  }

  getList(list_name) {
    return this.httpClient.get(`${this.api_url}${list_name}/`);
  }

  getItem(list_name, item_id) {
    return this.httpClient.get(`${this.api_url}${list_name}/${item_id}/`);
  }

  createItem(list_name, data){
     return this.httpClient.post(`${this.api_url}${list_name}/`, data);
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
