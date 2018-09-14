import {Component, Input, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-car-modal',
  templateUrl: './car-modal.component.html',
  styleUrls: ['./car-modal.component.css']
})
export class CarModalComponent implements OnInit {
  @Input() title: string;
  @Input() car: any;
  error: object;
  colours: Array<object>;

  constructor(public activeModal: NgbActiveModal,
              public apiService: ApiService,) {
  }

  ngOnInit() {
    this.apiService.getList('colours').subscribe((response: Array<object>) => {
      console.log(response);
      this.colours = response;
    });
  }

  public submitCar(data) {
    if (this.title == 'Edit car') {
      this.apiService.editItem('cars', this.car.id, data).subscribe((response) => {
        console.log(response);
        if (response) {
          this.activeModal.close();
          this.error = null;
        }
        else
          this.error = this.apiService.errorLog.pop();
      })
    }
    else if (this.title == 'Create car') {
      this.apiService.createItem('cars', data).subscribe((response) => {
        console.log(response);
        if (response) {
          this.activeModal.close();
          this.error = null;
        }
        else
          this.error = this.apiService.errorLog.pop();
      })
    }
  }

}
