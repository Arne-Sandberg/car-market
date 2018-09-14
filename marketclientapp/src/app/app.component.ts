import {Component, OnInit} from '@angular/core';
import {ApiService} from "./api.service";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {LoginModalComponent} from "./login-modal/login-modal.component";
import {RegisterModalComponent} from "./register-modal/register-modal.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {

  constructor(public apiService: ApiService,
              private modalService: NgbModal,) {
  }

  ngOnInit() {
    this.getCurrentUser();
    this.getBrands();
  }

  private getCurrentUser(): void {
    this.apiService.getMe().subscribe((response: object) => {
      console.log(response);
      if (response)
        this.apiService.currentUser = response;
    });
  }

  private getBrands(): void {
    this.apiService.getList('brands').subscribe((response: Array<object>) => {
      console.log(response);
      if (response)
        this.apiService.brands = response;
    });
  }

  public openLoginModal() {
    this.modalService.open(LoginModalComponent);
  }

  public openRegisterModal() {
    this.modalService.open(RegisterModalComponent);
  }

  public logout(): void {
    this.apiService.logout().subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.apiService.currentUser = null;
      }
    });
  }
}
