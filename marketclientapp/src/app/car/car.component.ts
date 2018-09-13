import {Component, OnInit} from '@angular/core';
import {ApiService} from '../api.service';
import {ActivatedRoute} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {EditCommentModalComponent} from "../edit-comment-modal/edit-comment-modal.component";

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent implements OnInit {
  car: object;
  error: object;
  modal;

  constructor(public apiService: ApiService,
              private modalService: NgbModal,
              private route: ActivatedRoute,) {
  }

  ngOnInit() {
    this.getCar();
  }

  public openModal(comment): void {
    let modal = this.modalService.open(EditCommentModalComponent);
    modal.componentInstance.carId = this.car['id'];
    modal.componentInstance.commentId = comment['id'];
    modal.componentInstance.commentContent = comment['content'];
    modal.componentInstance.commentRating = comment['rating'];
    modal.result.then(() => {
      this.getCar();
    });
  }

  public deleteComment(id: number): void {
    this.apiService.deleteItem('comments', id).subscribe((response: object) => {
      console.log(response);
      this.getCar();
    });
  }


  public createComment(form): void {
    let data = form.value;
    data['car'] = this.car['id'];
    this.apiService.createItem('comments', data).subscribe((response: object) => {
      console.log(response);
      if (response) {
        this.getCar();
        this.error = null;
        form.reset();
      }
      else
        this.error = this.apiService.errorLog.pop();
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
