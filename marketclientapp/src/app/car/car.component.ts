import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {EditCommentModalComponent} from "../edit-comment-modal/edit-comment-modal.component";
import {CheckoutModalComponent} from "../checkout-modal/checkout-modal.component";
import {CheckoutResultModalComponent} from "../checkout-result-modal/checkout-result-modal.component";
import {LoginModalComponent} from "../login-modal/login-modal.component";
import {RegisterModalComponent} from "../register-modal/register-modal.component";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {
  car: any;
  error: object;

  constructor(public apiService: ApiService,
              private modalService: NgbModal,
              private route: ActivatedRoute,) {
  }

  ngOnInit() {
    this.getCar();
  }

  public openLoginModal() {
    this.modalService.open(LoginModalComponent);
  }

  public openRegisterModal() {
    this.modalService.open(RegisterModalComponent);
  }

  public openEditCommentModal(comment: any): void {
    let modal = this.modalService.open(EditCommentModalComponent);
    modal.componentInstance.comment = comment;
    modal.result.then(() => {
      this.getCar();
    }, () => {
      modal.close();
    });
  }

  public openStripeModal(): void {
    let checkoutModal = this.modalService.open(CheckoutModalComponent);
    checkoutModal.componentInstance.email = this.apiService.currentUser.email;
    checkoutModal.componentInstance.car = this.car;
    checkoutModal.result.then((result) => {
      if (result) {
        let resultModal = this.modalService.open(CheckoutResultModalComponent);
        if (result == 'success') {
          this.getCar();
          resultModal.componentInstance.message =
            `Successfully purchased ${this.car.brand} - ${this.car.car_model} - ${this.car.car_type}.`;
        }
        else if (result == 'error') {
          resultModal.componentInstance.message =
            `Error occurred while purchasing ${this.car.brand} - ${this.car.car_model} - ${this.car.car_type}.`;
        }
      }
    }, () => {
      checkoutModal.close();
    });
  }

  public deleteComment(id: number): void {
    this.apiService.deleteItem('comments', id).subscribe((response: object) => {
      console.log(response);
      this.getCar();
    });
  }

  public createComment(form: any): void {
    let data = form.value;
    data.car = this.car.id;
    this.apiService.createItem('comments', data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.getCar();
        this.error = null;
        form.reset();
      }
      else
        this.error = this.apiService.errorLog.pop();
    });
  }

  private getCar(): void {
    this.apiService.getItem('cars', this.route.snapshot.paramMap.get('id'))
      .subscribe((response: any) => {
        console.log(response);
        if (response) {
          this.car = response;
          this.car.brand = this.apiService.brands.find(brand => brand.id == this.car.brand).name;
        }
        else
          this.error = this.apiService.errorLog.pop();
      });
  }
}
