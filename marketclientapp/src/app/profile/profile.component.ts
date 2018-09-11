import {Component, OnInit} from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  info: object;
  file_to_upload: File;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.getMe()
  }

  public getMe(): void {
    this.apiService.getMe().subscribe((response: object) => {
      this.info = response;
      console.log(response);
    });
  }

  public edit(data): void {
    let form_data: FormData = new FormData();
    for (let key in data)
      form_data.append(key, data[key]);
    if (this.file_to_upload)
      form_data.append('image', this.file_to_upload);
    this.apiService.editMe(form_data).subscribe((response: object) => {
      console.log(response);
      this.info = response;
    });
  }

  handleFileInput(file: FileList) {
    this.file_to_upload = file.item(0);
  }
}

