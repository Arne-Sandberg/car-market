import {Component, OnInit} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  url: string = 'http://127.0.0.1:8000/api/v1/logout';
  error: object;
  currentUserId: number;
  modal;

  constructor(private apiService: ApiService,
              private modalService: NgbModal,
              private router: Router,) {
  }

  ngOnInit() {
    this.getCurrentUser();
  }

  private getCurrentUser(redirect: boolean = false): void {
    this.apiService.getMe().subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.apiService.currentUser = response;
        this.currentUserId = this.apiService.currentUser['id'];
        if (redirect) {
          this.router.navigateByUrl(`/users/${this.currentUserId}`);
        }
      }
    });
  }

  public closeModal(): void {
    this.modal.close();
  }

  public openModal(content): void {
    this.error = null;
    this.modal = this.modalService.open(content);
  }

  private validateResponse(response: object): void {
    console.log(response);
    if (response) {
      this.closeModal();
      this.getCurrentUser(true);
      this.error = null;
    }
    else
      this.error = this.apiService.errorLog.pop();
  }

  public login(data): void {
    this.apiService.login(data).subscribe((response: object) => {
      this.validateResponse(response);
    });
  };

  public register(data): void {
    this.apiService.register(data).subscribe((response: object) => {
      this.validateResponse(response);
    });
  };

  public logout(): void {
    this.apiService.logout().subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.apiService.currentUser = null;
        this.currentUserId = null;
      }
    });
  }
}
