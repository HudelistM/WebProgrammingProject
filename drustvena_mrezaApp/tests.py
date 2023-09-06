# Django Testing Modules
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Application Modules
from drustvena_mrezaApp.views import pocetna
from drustvena_mrezaApp.profile_views import profil, lista_profila
from drustvena_mrezaApp.post_views import edit_post, delete_post, moj_profil, lista_objava
from drustvena_mrezaApp.models import Profil, Objava, stvori_profil  # Make sure to import stvori_profil if not already

class TestUrls(SimpleTestCase):

    def test_pocetna_url_resolves(self):
        url = reverse('drustvena_mrezaApp:pocetna')
        self.assertEqual(resolve(url).func, pocetna)

    def test_lista_profila_url_resolves(self):
        url = reverse('drustvena_mrezaApp:lista_profila')
        self.assertEqual(resolve(url).func, lista_profila)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_pocetna_GET(self):
        response = self.client.get(reverse('drustvena_mrezaApp:pocetna'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pocetna.html')

    def test_lista_profila_GET(self):
        response = self.client.get(reverse('drustvena_mrezaApp:lista_profila'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drustvena_mreza/lista_profila.html')

class TestObjavaModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser_objava', password='12345')
        cls.objava = Objava.objects.create(user=cls.user, sadrzaj='Test content', category='tech')

    def test_objava_creation(self):
        expected_str = f"{self.user.username} ({self.objava.datum_objave:%Y-%m-%d %H:%M}): "  # Note the added ': '
        self.assertEqual(str(self.objava), expected_str)

class TestProfilModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        post_save.disconnect(stvori_profil, sender=User)  # Disconnecting the signal
        cls.user = User.objects.create_user(username='testuser_profil', password='12345')
        cls.profil = Profil.objects.create(user=cls.user)

    def test_profil_creation(self):
        self.assertEqual(str(self.profil), self.user.username)

    def tearDown(self):
        post_save.connect(stvori_profil, sender=User)  # Reconnecting the signal

class TestFollowUnfollow(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Disconnect the signal to avoid double Profil creation
        post_save.disconnect(stvori_profil, sender=User)
        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')
        cls.profile1 = Profil.objects.create(user=cls.user1)
        cls.profile2 = Profil.objects.create(user=cls.user2)
        # Reconnect the signal
        post_save.connect(stvori_profil, sender=User)

    def test_follow_unfollow(self):
        self.profile1.follows.add(self.profile2)
        self.assertIn(self.profile2, self.profile1.follows.all())
        
        self.profile1.follows.remove(self.profile2)
        self.assertNotIn(self.profile2, self.profile1.follows.all())