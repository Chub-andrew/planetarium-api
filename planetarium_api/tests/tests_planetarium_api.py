from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium_api.models import PlanetariumDome
from planetarium_api.serializers import PlanetariumDomeSerializer

URL = reverse("planetarium:planetarium-dome-list")


def detail_url(planetarium_id):
    return reverse("planetarium:planetarium-dome-detail", args=(planetarium_id,))


def sample_planetarium_dome(**params) -> PlanetariumDome:
    defaults = {
        "name": "Superman-home",
        "rows": 5,
        "seats_in_row": 6,
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**defaults)


class UnauthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )
        self.client.force_authenticate(user=self.user)

    def test_planetarium_dome_list(self):
        sample_planetarium_dome()
        sample_planetarium_dome(name="GreenLantern-home",)
        res = self.client.get(URL)
        domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(domes, many=True)
        self.assertEquals(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_planetarium_dome_detail(self):
        planetarium = sample_planetarium_dome()
        url = detail_url(planetarium.id)
        res = self.client.get(url)

        serializer = PlanetariumDomeSerializer(planetarium)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_create_planetarium_forbidden(self):
        payload = {
            "name": "GreenLantern-home",
            "rows": 5,
            "seats_in_row": 6,
        }

        res = self.client.post(URL, payload)
        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password", is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_planetarium_dome_create(self):
        payload = {
            "name": "GreenLantern-home",
            "rows": 5,
            "seats_in_row": 6,
        }
        res = self.client.post(URL, payload)
        planetarium = PlanetariumDome.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(planetarium, key))
