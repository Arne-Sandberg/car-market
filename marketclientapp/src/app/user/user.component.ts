import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute, Router} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {EditProfileModalComponent} from "../edit-profile-modal/edit-profile-modal.component";
import {CarModalComponent} from "../car-modal/car-modal.component";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  user: any;
  error: object;
  cars: Array<object>;
  clientId: string = 'ca_DQaOCFCjDd2o48wUjD5fLPQlm6vkG51j';
  connectStripeUrl: string;

  constructor(private apiService: ApiService,
              private modalService: NgbModal,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.getUser();
  }

  public openEditProfileModal(): void {
    let modal = this.modalService.open(EditProfileModalComponent);
    modal.componentInstance.user = this.user;
    modal.result.then(() => {
      this.getUser();
    }, () => {
      modal.close();
    });
  }

  public openCreateCarModal(): void {
    let modal = this.modalService.open(CarModalComponent);
    modal.componentInstance.title = 'Create car';
    modal.result.then(() => {
      this.getUser();
    }, () => {
      modal.close();
    });
  }

  public openEditCarModal(car: any): void {
    let modal = this.modalService.open(CarModalComponent);
    modal.componentInstance.car = car;
    modal.componentInstance.title = 'Edit car';
    modal.result.then(() => {
      this.getUser();
    }, () => {
      modal.close();
    });
  }

  public isOwner(): boolean {
    return this.apiService.currentUser ? this.apiService.currentUser.id == this.user.id : false;
  }

  public getUser(): void {
    this.apiService.getItem('users', this.route.snapshot.paramMap.get('id'))
      .subscribe((response: object) => {
        console.log(response);
        if (response) {
          this.user = response;
          this.connectStripeUrl = `https://connect.stripe.com/oauth/authorize?response_type=code&client_id=${this.clientId}&scope=read_write&state=http://127.0.0.1:8000/angular/profile/${this.user.id}`
        }
        else
          this.error = this.apiService.errorLog.pop();
      });
  }

  public deleteCar(id: number): void {
    this.apiService.deleteItem('cars', id).subscribe((response: object) => {
      console.log(response);
      this.getUser();
    });
  }

}
