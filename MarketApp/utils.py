import stripe
from django.utils import timezone

from Market import settings
from MarketApp import models


def create_charge(request, car_id, token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    car = models.Car.objects.get(id=car_id)
    car.stock_count -= 1
    try:
        if car.user:
            stripe.Charge.create(
                amount=int(car.price * 92.9 + 30),
                currency="usd",
                source=token,
                description=f"{car} {car.colour} was sold to {request.user}",
                application_fee=int(car.price * 7.1 - 30),
                stripe_account=car.user.stripe_user_id,
            )
        else:
            stripe.Charge.create(
                amount=car.price * 100,
                currency="usd",
                source=token,
                description=f"{car} {car.colour} was sold to {request.user}",
            )
    except stripe.error.CardError:
        return False
    else:
        models.Purchase.objects.create(user=request.user, price=car.price, date=timezone.now(), car=car)
        car.save()
        return True
