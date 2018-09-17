import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {Observable} from "rxjs";
import {of} from 'rxjs/observable/of';

@Injectable()
export class ApiService {
  apiUrl: string = 'http://127.0.0.1:8000/api/v1/';
  errorLog: Array<object> = [];
  brands: Array<any>;
  currentUser: any;

  constructor(private httpClient: HttpClient) {
  }

  private handleError<T>(result?: T) {
    return (response: any): Observable<T> => {
      console.log(response);
      this.errorLog.push(response.error);
      return of(result as T);
    };
  }

  private getHttpOptions() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      const re = new RegExp('^csrftoken=');
      if (re.test(cookie)) {
        return {headers: new HttpHeaders({'X-CSRFTOKEN': cookie.substr(10, cookie.length)})}
      }
    }
  }

  getList(list_name) {
    return this.httpClient.get(`${this.apiUrl}${list_name}/`)
      .pipe(catchError(this.handleError()));
  }

  getItem(list_name, item_id) {
    return this.httpClient.get(`${this.apiUrl}${list_name}/${item_id}/`)
      .pipe(catchError(this.handleError()));
  }

  getMe() {
    return this.httpClient.get(`${this.apiUrl}me/`)
      .pipe(catchError(this.handleError()));
  }

  editMe(data) {
    return this.httpClient.put(`${this.apiUrl}me/`, data, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  editItem(list_name, id, data) {
    return this.httpClient.put(`${this.apiUrl}${list_name}/${id}/`, data, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  createItem(list_name, data) {
    return this.httpClient.post(`${this.apiUrl}${list_name}/`, data, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  deleteItem(list_name, id) {
    return this.httpClient.delete(`${this.apiUrl}${list_name}/${id}/`, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  register(data) {
    return this.httpClient.post(`${this.apiUrl}register/`, data, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  login(data) {
    return this.httpClient.post(`${this.apiUrl}login/`, data, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }

  logout() {
    return this.httpClient.post(`${this.apiUrl}logout/`, null, this.getHttpOptions())
      .pipe(catchError(this.handleError()));
  }
}
