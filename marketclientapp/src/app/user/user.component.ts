import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  user: object;
  cars: Array<object>;
  error: object;
  fileToUpload: File;
  modal;

  constructor(private apiService: ApiService,
              private modalService: NgbModal,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.getUser();
  }

  public closeModal(): void {
    this.modal.close();
  }

  public openModal(content): void {
    this.error = null;
    this.modal = this.modalService.open(content);
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

  public edit(data): void {
    let form_data: FormData = new FormData();
    for (let key in data)
      form_data.append(key, data[key]);
    if (this.fileToUpload)
      form_data.append('image', this.fileToUpload);
    this.apiService.editMe(form_data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.closeModal();
        this.error = null;
        this.user = response;
      }
      else
        this.error = this.apiService.errorLog.pop();
    });
  }

  handleFileInput(file: FileList) {
    this.fileToUpload = file.item(0);
  }
}
