import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  ads: Array<object>;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getAds();
  }

  public getAds() {
    this.apiService.getList('adds').subscribe((response: Array<object>) => {
      console.log(response);
      if (response)
        this.ads = response;
    });
  }
}
