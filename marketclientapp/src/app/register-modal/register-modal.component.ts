import {Component, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register-modal',
  templateUrl: './register-modal.component.html',
  styleUrls: ['./register-modal.component.css']
})
export class RegisterModalComponent implements OnInit {
  error: object;

  constructor(private activeModal: NgbActiveModal,
              private apiService: ApiService,
              private router: Router,) {
  }

  ngOnInit() {
  }


  public register(data): void {
    this.apiService.register(data).subscribe((response: object) => {
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
