import {Component, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login-modal',
  templateUrl: './login-modal.component.html',
  styleUrls: ['./login-modal.component.css']
})
export class LoginModalComponent implements OnInit {
  error: object;

  constructor(private activeModal: NgbActiveModal,
              private apiService: ApiService,
              private router: Router,) {
  }

  ngOnInit() {
  }

  public login(data): void {
    this.apiService.login(data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.activeModal.close();
        this.apiService.getMe().subscribe((response: object) => {
          console.log(response);
          if (response) {
            this.apiService.currentUser = response;
            this.router.navigateByUrl(`/users/${response['id']}`);
          }
        });
        this.error = null;
      }
      else
        this.error = this.apiService.errorLog.pop();
    });
  };
}
