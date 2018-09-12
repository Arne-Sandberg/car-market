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
  @Input() info: object;
  @Input() owner: boolean;
  image: string;
  cars: Array<object>;
  purchases: Array<object>;
  infoKeys: Array<string>;
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

  public closeModal() {
    this.modal.close();
  }

  public openModal(content) {
    this.error = null;
    this.modal = this.modalService.open(content);
  }

  public getUser(): void {
    if (!this.info) {
      this.apiService.getItem('users', this.route.snapshot.paramMap.get('id')).subscribe((response: object) => {
        console.log(response);
        if (response) {
          this.info = response;
          this.image = this.info['image'];
          this.infoKeys = Object.keys(this.info).filter(
            key => !['image', 'id', 'car_set', 'purchase_set',].includes(key));
        }
        else
          this.error = this.apiService.log.pop();
      });
    }
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
        this.info = response;
      }
      else
        this.error = this.apiService.log.pop();
    });
  }

  handleFileInput(file: FileList) {
    this.fileToUpload = file.item(0);
  }
}
