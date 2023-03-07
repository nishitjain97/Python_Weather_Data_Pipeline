from django.test import TestCase

from .models import Weather, Stats

from django.urls import reverse

class WeatherViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create data for testing
        number_of_records = 20

        for record in range(number_of_records):
            Weather.objects.create(
                id = record,
                Date = 19850101,
                Maxtemp = -83,
                Mintemp = -144,
                Precipitation = 0,
                Station_id = 'USC00257715'
            )

    def test_view_url_exists(self):
        # Test existance of URL
        response = self.client.get('/api/weather')
        return self.assertEqual(response.status_code, 200)
    
    def test_view_url_by_name(self):
        # Test if URL exists by name
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        # Test for pagination
        response = self.client.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('"has_next": true' in str(response.content))

class StatsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create data for testing
        number_of_records = 20

        for record in range(number_of_records):
            Stats.objects.create(
                id = record,
                Year = 1985,
                Average_Maxtemp = 192.04029304029305,
                Average_Mintemp = 66.96703296703296,
                Sum_Precipitation = 7985.0,
                Station_id = 'USC00112193'
            )

    def test_view_url_exists(self):
        # Test existance of URL
        response = self.client.get('/api/weather/stats')
        return self.assertEqual(response.status_code, 200)
    
    def test_view_url_by_name(self):
        # Test if URL exists by name
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        # Test for pagination
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('"has_next": true' in str(response.content))