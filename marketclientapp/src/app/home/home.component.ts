import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  ads: Array<any>;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getAds();
  }

  public getAds() {
    this.apiService.getList('adds').subscribe((response: Array<any>) => {
      console.log(response);
      if (response) {
        this.ads = response;
        for (let car of this.ads)
          car.brand = this.apiService.brands.find(brand => brand.id == car.brand).name;
      }
    });
  }
}
