from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from datetime import date

from petstagram.petstagram.common.models import PhotoLike
from petstagram.petstagram.pets.models import Pet
from petstagram.petstagram.photos.models import Photo

"""

1.User is owner
2.User is not owner
3.User has no pets
4.User has pets, no photos
5.User has pets and 1 photo
6.User has pets and 2 photos
7.User has pets and 7 photos, and page is default
8.User has pets and 7 photos, and page is 1
9.User has pets and 7 photos, and page is 2
10.User has no likes
11.User has likes for a single pet
12.User has likes for a multiple pets

"""

UserModel = get_user_model()


def create_pets_for_user(user, count=5):
    result = [Pet(
        name=f'Pet {i + 1}',
        personal_photo=f'http://pets.com/{i + 1}.jpg',
        date_of_birth=date(2015 + i, (1 + i) % 12, (1 + i) % 28),
        user=user,
    ) for i in range(count)]

    [p.save() for p in result]

    return result


def create_photo_for_user_and_pets(user, pets, count=5):
    photos = [Photo(
        photo=f'/var/images/img - {i + 1}.png',
        user=user,
    ) for i in range(count)]

    for photo in photos:
        photo.save()
        for pet in pets:
            photo.tagged_pets.add(pet)
        photo.save()

    return photos


def create_photo_likes_for_user_and_photos(user, photos):
    current = 0
    total_likes_count = 0

    for photo in photos:
        for i in range(current):
            PhotoLike(
                photo=photo,
                user=user,
            ).save()

            total_likes_count += 1
        current += 1

    return total_likes_count


class UserDetailsViewTests(TestCase):
    VALID_USER_DATA = {
        'username': 'test_user',
        'email': 'test_user@petstagram.tk',
        'password': '1234qwe',
    }

    def assertEmpty(self, collection):
        return self.assertEqual(0, len(collection), 'It is not empty')

    def _create_user_and_login(self, user_data):
        user = UserModel.objects.create_user(**user_data)
        self.client.login(**self.VALID_USER_DATA)
        return user

    def test_user_details__when_owner__expect_is_owner_true(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)
        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_user_details__when_not_owner__expect_is_owner_false(self):
        profile_user = self._create_user_and_login({
            'username': self.VALID_USER_DATA['username'] + '1',
            'email': self.VALID_USER_DATA['email'] + '1',
            'password': self.VALID_USER_DATA['password'] + '1'
        })

        self._create_user_and_login(self.VALID_USER_DATA)

        response = self.client.get(reverse_lazy('details user', kwargs={'pk': profile_user.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_user_details__when_no_pets__expect_empty_pets(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)
        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEmpty(response.context['pets'])

    def test_user_details__when_pets_and_no_photo__expect_pets_and_no_photos(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        create_pets_for_user(user, count=5)

        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEqual(5, len(response.context['pets']))
        self.assertEmpty(response.context['photos'])

    def test_user_details__when_pets_and_1_photo__expect_pets_1_photo(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        pets = create_pets_for_user(user, count=5)
        photos = create_photo_for_user_and_pets(user, pets=pets[:2], count=1)

        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEqual(5, len(response.context['pets']))
        self.assertEqual(1, len(response.context['photos']))
        self.assertListEqual(list(photos), list(response.context['photos']))
        self.assertEqual(0, response.context['photos_count'])

    def test_user_details__when_pets_and_2_photos__expect_pets_2_photos(self):
        pass

    def test_user_details__when_pets_and_7_photos__expect_pets_7_photos(self):
        pass

    def test_user_details__when_pets_and_7_photos_page_1__expect_pets_7_photos(self):
        pass

    def test_user_details__when_pets_and_7_photos_page_2__expect_pets_7_photos(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        pets = create_pets_for_user(user, count=5)
        photos = create_photo_for_user_and_pets(user, pets=pets[:2], count=7)

        response = self.client.get(
            reverse_lazy('details user', kwargs={'pk': user.pk}),
            data={
                'page': 2
            })

        self.assertListEqual(pets, list(response.context['pets']))
        self.assertListEqual(photos[2:4], list(response.context['photos']))
        self.assertEqual(7, response.context['photos_count'])

    def test_user_details__when_no_likes__expect_0_likes_count(self):
        pass

    def test_user_details__when_likes_for_single_pet__expect_correct_likes_count(self):
        pass

    def test_user_details__when_likes_for_multiple_pets__expect_combined_likes_count(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        pets = create_pets_for_user(user, count=5)
        photos = create_photo_for_user_and_pets(user, pets=pets[:2], count=7)
        total_likes_count = create_photo_likes_for_user_and_photos(user, photos)

        response = self.client.get(
            reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEqual(total_likes_count + 1, response.context['likes_count'])
