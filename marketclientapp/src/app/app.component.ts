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
  isAuthenticated: boolean = false;
  modal;

  constructor(private apiService: ApiService,
              private modalService: NgbModal,
              private router: Router) {
  }

  ngOnInit() {
    this.apiService.getMe().subscribe((response: object) => {
      console.log(response);
      if (response)
        this.isAuthenticated = true;
    });
  }

  public closeModal() {
    this.modal.close();
  }

  public openModal(content) {
    this.error = null;
    this.modal = this.modalService.open(content);
  }

  public login(data): void {
    this.apiService.login(data).subscribe((response) => {
      console.log(response);
      if (response) {
        this.closeModal();
        this.error = null;
        this.router.navigateByUrl('/profile');
        this.isAuthenticated = true;
      }
      else
        this.error = this.apiService.log.pop();
    });
  };

  public register(data): void {
    this.apiService.register(data).subscribe((response) => {
      console.log(response);
      if (response) {
        this.closeModal();
        this.error = null;
        this.router.navigateByUrl('/profile');
        this.isAuthenticated = true;
      }
      else {
        this.error = this.apiService.log.pop();
      }
    });
  };

  public logout(): void {
    this.apiService.logout().subscribe((response) => {
      console.log(response);
      this.isAuthenticated = false;
    });
  }
}
