import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {
  car: object;
  error: object;
  editError: object;
  createError: object;
  editingCommentId: number;
  editingCommentContent: string;
  editingCommentRating: number;
  modal;

  constructor(public apiService: ApiService,
              private modalService: NgbModal,
              private route: ActivatedRoute,) {
  }

  ngOnInit() {
    this.getCar();
  }

  public closeModal(): void {
    this.editingCommentId = null;
    this.modal.close();
  }

  public openModal(content, comment): void {
    this.editError = null;
    this.editingCommentId = comment.id;
    this.editingCommentContent = comment.content;
    this.editingCommentRating = comment.rating;
    this.modal = this.modalService.open(content);
  }

  public deleteComment(id: number): void {
    this.apiService.deleteItem('comments', id).subscribe((response: object) => {
      console.log(response);
      this.getCar();
    });
  }

  public editComment(data): void {
    data['car'] = this.car['id'];
    this.apiService.editItem('comments', this.editingCommentId, data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.closeModal();
        this.getCar();
        this.editError = null;
      }
      else
        this.editError = this.apiService.errorLog.pop();
    });
  }

  public createComment(form): void {
    let data = form.value;
    data['car'] = this.car['id'];
    this.apiService.createItem('comments', data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.getCar();
        this.createError = null;
        form.reset();
      }
      else
        this.createError = this.apiService.errorLog.pop();
    });
  }

  public getCar(): void {
    this.apiService.getItem('cars', this.route.snapshot.paramMap.get('id'))
      .subscribe((response: object) => {
        console.log(response);
        response ? this.car = response : this.error = this.apiService.errorLog.pop();
      });
  }
}
