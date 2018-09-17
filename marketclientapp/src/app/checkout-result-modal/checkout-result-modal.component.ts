import {Component, Input, OnInit} from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-checkout-result-modal',
  templateUrl: './checkout-result-modal.component.html',
  styleUrls: ['./checkout-result-modal.component.css']
})
export class CheckoutResultModalComponent implements OnInit {
  @Input() message: string;

  constructor(public activeModal: NgbActiveModal,) {
  }

  ngOnInit() {
  }

}
