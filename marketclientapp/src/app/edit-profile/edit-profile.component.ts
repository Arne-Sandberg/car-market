import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent implements OnInit {
  info: object;
  fileToUpload: File;
  error: object;

  constructor(private apiService: ApiService,
              private router: Router) {
  }

  ngOnInit() {
    this.getMe()
  }

  public getMe(): void {
    this.apiService.getMe().subscribe((response: object) => {
      console.log(response);
      if (response)
        this.info = response;
    });
  }

  public edit(data): void {
    let form_data: FormData = new FormData();
    for (let key in data)
      form_data.append(key, data[key]);
    if (this.fileToUpload)
      form_data.append('image', this.fileToUpload);
    this.apiService.editMe(form_data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.info = response;
        this.router.navigateByUrl('/profile');
      }
      else
        this.error = this.apiService.log.pop();
    });
  }

  handleFileInput(file: FileList) {
    this.fileToUpload = file.item(0);
  }
}
