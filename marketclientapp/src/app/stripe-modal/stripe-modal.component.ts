import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {
  StripeService,
  ElementOptions,
  ElementsOptions,
  StripeCardComponent
} from "ngx-stripe";
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-stripe-modal',
  templateUrl: './stripe-modal.component.html',
  styleUrls: ['./stripe-modal.component.css']
})
export class StripeModalComponent implements OnInit {
  @ViewChild(StripeCardComponent) card: StripeCardComponent;
  @Input() email: string;
  @Input() car: any;
  error: any;
  elementsOptions: ElementsOptions = {
    locale: 'en'
  };
  cardOptions: ElementOptions = {
    style: {
      base: {
        iconColor: '#4B5EFF',
        color: '#000000',
        fontWeight: 300,
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '18px',
        '::placeholder': {
          color: '#A9AFFF'
        }
      }
    }
  };


  constructor(private stripeService: StripeService,
              private apiService: ApiService,
              public activeModal: NgbActiveModal,) {
  }

  ngOnInit() {
  }

  public buy() {
    this.stripeService.createToken(this.card.getCard(), {name: this.email}).subscribe((result: any) => {
      console.log(result);
      if (result.error)
        this.error = result.error;
      else {
        let formData: FormData = new FormData();
        formData.append('car', this.car.id);
        formData.append('stripe_token', result.token.id);
        formData.append('stripe_email', result.token.card.name);
        this.apiService.createItem('checkout', formData).subscribe((result: any) => {
          console.log(result);
          this.activeModal.close();
          alert(result ? `Successfully purchased ${this.car.brand} - ${this.car.car_model} - ${this.car.car_type}.`
            : 'Something went wrong. Try again.');
        });
      }
    });
  }
}
