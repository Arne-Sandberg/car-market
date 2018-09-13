import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {EditProfileModalComponent} from "../edit-profile-modal/edit-profile-modal.component";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  user: object;
  cars: Array<object>;
  error: object;
  modal;

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

  public isOwner(): boolean {
    return this.apiService.currentUser ? this.apiService.currentUser['id'] == this.user['id'] : false;
  }

  public getUser(): void {
    this.apiService.getItem('users', this.route.snapshot.paramMap.get('id'))
      .subscribe((response: object) => {
        console.log(response);
        response ? this.user = response : this.error = this.apiService.errorLog.pop();
      });
  }

  public deleteCar(id): void {
    this.apiService.deleteItem('cars', id).subscribe((response: object) => {
      console.log(response);
      this.getUser();
    });
  }

}
