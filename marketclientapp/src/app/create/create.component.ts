import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {
  formName: string;
  colours: Array<object>;
  cars: Array<object>;
  brands: Array<object>;
  listArr: Array<string> = ['cars', 'comments'];

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.apiService.getList('colours').subscribe((response: Array<object>) => {
      console.log(response);
      this.colours = response;
    });
    this.apiService.getList('cars').subscribe((response: Array<object>) => {
      console.log(response);
      this.cars = response;
    });
    this.apiService.getList('brands').subscribe((response: Array<object>) => {
      console.log(response);
      this.brands = response;
    });
  }

  public createItem(data): void {
    this.apiService.createItem(this.formName, data).subscribe((response => {
        console.log(response);
      })
    );
  }

  public showForm(list_name): void {
    this.formName = list_name;
  }
}
