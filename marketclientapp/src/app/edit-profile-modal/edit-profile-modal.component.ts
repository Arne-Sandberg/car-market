import {Component, Input, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-edit-profile-modal',
  templateUrl: './edit-profile-modal.component.html',
  styleUrls: ['./edit-profile-modal.component.css']
})
export class EditProfileModalComponent implements OnInit {
  @Input() user: object;
  fileToUpload: File;
  error: object;

  constructor(private activeModal: NgbActiveModal,
              private apiService: ApiService) {
  }

  ngOnInit() {
  }

  public editMe(data): void {
    let formData: FormData = new FormData();
    for (let key in data)
      formData.append(key, data[key]);
    if (this.fileToUpload)
      formData.append('image', this.fileToUpload);
    this.apiService.editMe(formData).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.activeModal.close();
        this.error = null;
      }
      else
        this.error = this.apiService.errorLog.pop();
    });
  }

  public handleFileInput(file: FileList) {
    this.fileToUpload = file.item(0);
  }
}
