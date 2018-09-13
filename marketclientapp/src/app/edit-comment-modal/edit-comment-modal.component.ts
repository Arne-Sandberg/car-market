import {Component, Input, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-edit-comment-modal',
  templateUrl: './edit-comment-modal.component.html',
  styleUrls: ['./edit-comment-modal.component.css']
})
export class EditCommentModalComponent implements OnInit {
  @Input() comment: object;
  error: object;

  constructor(public activeModal: NgbActiveModal,
              private apiService: ApiService,) {
  }

  ngOnInit() {
  }

  public editComment(data): void {
    data['car'] = this.comment['car'];
    this.apiService.editItem('comments', this.comment['id'], data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.activeModal.close();
        this.error = null;
      }
      else
        this.error = this.apiService.errorLog.pop();
    });
  }

}
