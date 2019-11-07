from django.test import TestCase
from .models import HealthData,Person
from django.contrib.auth.models import User
from django.urls import reverse

class UserTestCase(TestCase):
    def create_user(self,username="guest",password="1DS8ylMMP"):
        u = User.objects.create(username=username,password=password)
        u.save()
        return u
    def test_create_user(self):
        u = self.create_user()
        self.assertTrue(isinstance(u,User))
    def test_login_user(self):
        u = self.create_user()
        url = reverse('login')
        resp = self.client.get(url)
        # check response code
        self.assertEqual(resp.status_code, 200)
        # check 'login' in response
        self.assertIn('Login'.encode(), resp.content)
        # log the user in
        self.user = u
        self.client.force_login(self.user)
        # check response code
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check logout in response
        url = reverse('home')
        self.assertIn('Logout'.encode(),resp.content)
    def test_logout_user(self):
        u = self.create_user()
        # log the user in
        self.user = u
        self.client.force_login(self.user)
        # check response code
        url = reverse('login')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Logout'.encode(),resp.content)
        # Log out
        url = reverse('logout')
        self.client.logout()
        # Check response code
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        # Check login in response
        url = reverse('home')
        self.assertIn('Login'.encode(),resp.content)

class PersonTestCase(TestCase):
    def create_person(self,name="guest",age=10,gender="Male",personalheight=160,personalweight=50):
        u = User.objects.create(username="guest",password="1DS8ylMMP")
        u.save()
        self.user=u
        self.client.force_login(self.user)
        return Person.objects.create(user=u,name=name,age=age,gender=gender,personalheight=personalheight,personalweight=personalweight)
    def test_create_person(self):
        p = self.create_person()
        self.assertTrue(isinstance(p,Person))
    def test_person_list_view(self):
        p = self.create_person()
        url = reverse('index',kwargs={'id':p.id})
        resp = self.client.get(url)
        # Check if response gives right p.id
        self.assertEqual(reverse('index',kwargs={'id':p.id}),p.get_absolute_url())
        self.assertEqual(resp.status_code, 200)
        # Check if response gives right p.name
        self.assertIn(p.name.encode(), resp.content)
    def test_person_update(self):
        p = self.create_person()
        url = reverse('update')
        resp = self.client.post(url,{'name':'guest','age':20,'gender':'Female','personalheight':162,'personalweight':48},follow=True)
        # Check if p has been modified
        self.assertIn(p.age,resp.content)
        # Check if redirected to the desired url
        self.assertRedirects(resp,'/ehealth/user/')

    def test_person_profile_view(self):
        p = self.create_person()
        url = reverse('user')
        resp = self.client.get(url)
        # Check Response code
        self.assertEqual(resp.status_code, 200)
        # Check if response gives right p.name
        self.assertIn(p.name.encode(), resp.content)

    def test_person_history_view(self):
        p = self.create_person()
        url = reverse('history')
        resp = self.client.get(url)
        # Check Response code
        self.assertEqual(resp.status_code, 200)
        # Check if response gives right p.name
        self.assertIn(p.name.encode(), resp.content)


class HealthDataTestCase(TestCase):
    def create_healthdata(self,originalEMG=['150','150'],frequencyEMG=['30','30'],mediafreq=130,temperature=37,spO2=90,pulse=100,fati=0):
        u = User.objects.create(username="guest",password="1DS8ylMMP")
        u.save()
        p = Person.objects.create(user=u,name="guest",age="10",gender="Male",personalheight="160",personalweight="50")
        p.save()
        return HealthData.objects.create(person=p,originalEMG=originalEMG,frequencyEMG=frequencyEMG,mediafreq=mediafreq,temperature=temperature,spO2=spO2,pulse=pulse,fati=fati)
    def test_create_healthdata(self):
        h = self.create_healthdata()
        self.assertTrue(isinstance(h,HealthData))
    def test_insert_healthdata(self):
        h = self.create_healthdata()
        url = reverse('insertion')
        resp = self.client.get(url,{'originalEMG':['150','150'],'frequencyEMG':['30','30'],'mediafreq':130,'temperature':37,'spO2':90,'pulse':100,'fati':0})
        # Check Response code
        self.assertEqual(resp.status_code, 200)
        # Check if the request stimulated by the response contains element query_string
        self.assertIn('QUERY_STRING',resp.request)
