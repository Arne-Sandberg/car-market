import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  error: object;

  constructor(private apiService: ApiService,
              private router: Router) {
  }

  ngOnInit() {
  }

  public register(data): void {
    this.apiService.register(data).subscribe((response) => {
      console.log(response);
      if (response)
        this.router.navigateByUrl('/profile');
      else {
        this.error = this.apiService.log.pop();
      }
    });
  };

}
