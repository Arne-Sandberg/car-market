from django.test import TestCase

from MarketApp.models import User, Car, Brand, Comment


def create_users():
    User.objects.create_user(username='test_user_1', password='qwe12345', email='testuser1@gmail.com')
    User.objects.create_user(username='test_user_2', password='qwe12345', email='testuser2@gmail.com')
    User.objects.create_user(username='test_user_3', password='qwe12345', email='testuser3@gmail.com')


def create_brands():
    Brand.objects.create(name='brand_1', owner='owner_1')
    Brand.objects.create(name='brand_2', owner='owner_2')


def create_cars():
    Car.objects.create(car_model='model_1', brand_id=1, year=2000, price=1000, colour='red')
    Car.objects.create(car_model='model_2', brand_id=1, year=2005, price=2000, colour='yellow')
    Car.objects.create(car_model='model_3', brand_id=1, year=2010, price=1500, colour='black')
    Car.objects.create(car_model='model_4', brand_id=2, year=2007, price=1700, colour='yellow')
    Car.objects.create(car_model='model_5', brand_id=2, year=2009, price=1600, colour='red')
    Car.objects.create(car_model='model_6', brand_id=2, year=2011, price=2000, colour='white')
    Car.objects.create(car_model='model_7', brand_id=2, year=2015, price=2100, colour='red')


def create_comments():
    Comment.objects.create(car_id=1, user_id=1, content='comment_1', rating=3)
    Comment.objects.create(car_id=1, user_id=2, content='comment_2', rating=5)
    Comment.objects.create(car_id=2, user_id=2, content='comment_3', rating=4)


class FilterTestCase(TestCase):
    def setUp(self):
        create_brands()
        create_cars()

    def test_filter_count(self):
        # filter - 2 items
        brand_id = 1
        response = self.client.get(f'/filter/{brand_id}/',
                                   {'min_year': 2000, 'max_year': 2010, 'in_stock_only': False, 'min_price': 1500,
                                    'max_price': 3000, 'colour': 'any colour', 'number_of_seats': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 2)

        # filter - 1 items
        brand_id = 2
        response = self.client.get(f'/filter/{brand_id}/',
                                   {'min_year': 2005, 'max_year': 2010, 'in_stock_only': False, 'min_price': 1000,
                                    'max_price': 2000, 'colour': 'yellow', 'number_of_seats': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 1)

        # cancel filter
        brand_id = 1
        response = self.client.get(f'/filter/{brand_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), len(Car.objects.filter(brand_id=brand_id)))


class IndexTestCase(TestCase):
    def setUp(self):
        create_brands()
        create_cars()

    def test_advertisement_count(self):
        # advertisement - no items (7 total)
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['advertisement']), 6)

        # advertisement - 2 items (8 total)
        Car.objects.create(car_model='model_8', brand_id=1, year=2000, price=1000, colour='red', is_advertised=True)
        car = Car.objects.get(id=1)
        car.is_advertised = True
        car.save()
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['advertisement']), 2)


class CommentsTestCase(TestCase):
    def setUp(self):
        create_brands()
        create_cars()
        create_users()
        create_comments()
        self.client.login(username='test_user_1', password='qwe12345')

    def test_comments_count(self):
        # comments - 2 items
        response = self.client.post('/comment/', {'car_id': 1, 'flag': 'refresh'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 2)

        # comments - 3 items
        response = self.client.post('/comment/', {'car_id': 1, 'flag': 'create', 'content': 'comment', 'rating': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 3)

        # comments - 4 items
        response = self.client.post('/comment/', {'car_id': 1, 'flag': 'create', 'content': 'comment', 'rating': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 4)

        # comments - 4 items
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'edit', 'content': 'edited comment', 'rating': 5,
                                     'comment_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 4)
        self.assertEqual(Comment.objects.get(id=1).content, 'edited comment')
        self.assertEqual(Comment.objects.get(id=1).rating, 5)

        # comments - 4 items
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'editing', 'content': 'old_content', 'rating': 5,
                                     'comment_id': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 4)

        # comments - 3 items
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'delete', 'comment_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object'].comment_set.all()), 3)
