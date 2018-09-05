import {Component, OnInit} from '@angular/core';
import {APIService} from "../api.service";

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {
  form_name: string;
  list_names: Array<string> = ['cars', 'comments'];

  constructor(private apiService: APIService) {
  }

  ngOnInit() {
  }

  public createItem(data) {
    console.log(data);
    this.apiService.createItem(this.form_name, data).subscribe((response => {
        console.log(response);
      })
    );
  }

  public showForm(list_name) {
    this.form_name = list_name;
  }
}
