import pytest

pytestmark = pytest.mark.django_db


class TestSubjects():
    @pytest.mark.parametrize('route,expected', [
        ('', 200),
        ('list/', 200),
        ('browse/', 200),
        ('search/', 200),
        ('about/', 200),
        ('untl-bs.json', 200),
        ('admin/', 302),
    ])
    def test_response_codes(self, client, route, expected):
        response = client.get('/subjects/%s' % (route))
        assert(response.status_code == expected)
