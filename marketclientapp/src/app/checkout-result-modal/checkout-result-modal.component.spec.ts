import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckoutResultModalComponent } from './checkout-result-modal.component';

describe('CheckoutResultModalComponent', () => {
  let component: CheckoutResultModalComponent;
  let fixture: ComponentFixture<CheckoutResultModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CheckoutResultModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CheckoutResultModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
