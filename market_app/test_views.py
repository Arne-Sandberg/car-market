from django.test import TestCase

from market_app.models import User, Car, Brand, Comment


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
        # filtering, displayed 2 items of brand#1
        brand_id = 1
        response = self.client.get(f'/filter/{brand_id}/',
                                   {'min_year': 2000, 'max_year': 2010, 'in_stock_only': False, 'min_price': 1500,
                                    'max_price': 3000, 'colour': 'any colour', 'number_of_seats': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 2)

        # filtering, displayed 1 item of brand#2
        brand_id = 2
        response = self.client.get(f'/filter/{brand_id}/',
                                   {'min_year': 2005, 'max_year': 2010, 'in_stock_only': False, 'min_price': 1000,
                                    'max_price': 2000, 'colour': 'yellow', 'number_of_seats': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), 1)

        # cancel filter, displayed items of brand#1- 3
        brand_id = 1
        response = self.client.get(f'/filter/{brand_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cars']), len(Car.objects.filter(brand_id=brand_id)))


class IndexTestCase(TestCase):
    def setUp(self):
        create_brands()
        create_cars()

    def test_advertisement_count(self):
        # advertising 0 items (7 total)
        response = self.client.get('/home')
        # displayed items - 6
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['advertisement']), 6)

        # advertising 2 items (8 total)
        Car.objects.create(car_model='model_8', brand_id=1, year=2000, price=1000, colour='red', is_advertised=True)
        car = Car.objects.get(id=1)
        car.is_advertised = True
        car.save()
        response = self.client.get('')
        # displayed items - 2
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['advertisement']), 2)


class CommentsTestCase(TestCase):
    def setUp(self):
        create_brands()
        create_cars()
        create_users()
        create_comments()
        self.client.login(username='test_user_1', password='qwe12345')

    def test_comment_delete(self):
        comment_count = Comment.objects.all().count() - 1
        car_comment_count = Car.objects.get(id=1).comment_set.all().count() - 1
        # deleting comment for car#1 (2 comments about car#1)
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'delete', 'comment_id': 1})
        self.assertEqual(response.status_code, 200)
        # comments displayed - 1
        self.assertEqual(response.context['object'].comment_set.all().count(), car_comment_count)
        # comments in DB - 2
        self.assertEqual(Comment.objects.all().count(), comment_count)

    def test_comment_create(self):
        comment_count = Comment.objects.all().count() + 1
        car_comment_count = Car.objects.get(id=1).comment_set.all().count() + 1
        # adding comment for car#1 (2 comments about car#1)
        response = self.client.post('/comment/', {'car_id': 1, 'flag': 'create', 'content': 'new comment', 'rating': 3})
        self.assertEqual(response.status_code, 200)
        # comments displayed - 3
        self.assertEqual(response.context['object'].comment_set.all().count(), car_comment_count)
        # comments in DB - 4
        self.assertEqual(Comment.objects.all().count(), comment_count)

    def test_comment_edit(self):
        comment_count = Comment.objects.all().count()
        car_comment_count = Car.objects.get(id=1).comment_set.all().count()
        # edit comment#1 for car#1 (2 comments about car#1)
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'edit', 'content': 'edited comment', 'rating': 5,
                                     'comment_id': 1})
        self.assertEqual(response.status_code, 200)
        # comments displayed - 2
        self.assertEqual(response.context['object'].comment_set.all().count(), car_comment_count)
        # comments in DB - 3
        self.assertEqual(Comment.objects.all().count(), comment_count)
        # checking if data for comment#1 has changed
        self.assertEqual(Comment.objects.get(id=1).content, 'edited comment')
        self.assertEqual(Comment.objects.get(id=1).rating, 5)

    def test_comment_editing(self):
        comment_count = Comment.objects.all().count()
        car_comment_count = Car.objects.get(id=1).comment_set.all().count()
        # editing comment#2 for car#1 (2 comments about car#1)
        response = self.client.post('/comment/',
                                    {'car_id': 1, 'flag': 'editing', 'content': 'old_content', 'rating': 2,
                                     'comment_id': 2})
        self.assertEqual(response.status_code, 200)
        # comments displayed - 2
        self.assertEqual(response.context['object'].comment_set.all().count(), car_comment_count)
        # comments in DB - 3
        self.assertEqual(Comment.objects.all().count(), comment_count)
        # data for comment#2 mustn't be changed yet
        self.assertNotEqual(Comment.objects.get(id=1).content, 'old_content')
        self.assertNotEqual(Comment.objects.get(id=1).rating, 2)
        # checking if data in form has changed
        self.assertEqual(int(response.context['form']['rating'].value()), 2)
        self.assertEqual(response.context['form']['content'].value(), 'old_content')

        # canceling editing comment#2 for car#1 (2 comments about car#1)
        response = self.client.post('/comment/', {'car_id': 1, 'flag': 'refresh'})
        self.assertEqual(response.status_code, 200)
        # comments displayed - 2
        self.assertEqual(response.context['object'].comment_set.all().count(), car_comment_count)
        # comments in DB - 3
        self.assertEqual(Comment.objects.all().count(), comment_count)
        # data for comment#2 mustn't be changed
        self.assertNotEqual(Comment.objects.get(id=1).content, 'old_content')
        self.assertNotEqual(Comment.objects.get(id=1).rating, 2)
        # checking if data in form has been cleaned
        self.assertEqual(int(response.context['form']['rating'].value()), 1)
        self.assertEqual(response.context['form']['content'].value(), None)
