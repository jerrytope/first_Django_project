from django.urls import path, include
from polls import views
urlpatterns = [
	path('', views.index, name= 'index'),
	path('about', views.about, name= 'about'),
	path('contact', views.contact, name= 'contact'),
	path('blogs', views.handleblog, name= 'handleblog'),
	path('blog', views.blog, name= 'blog'),
	path('service', views.service, name= 'service'),
	path('search', views.search, name= 'search'),
	path('login', views.handlelogin, name= 'handlelogin'),
	path('logout', views.handlelogout, name= 'handlelogout'),
	path('signup', views.handlesignup, name= 'handlesignup'),
 	path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
 	path('QandA/', views.QandA, name='QandA'),
    path('convert_to_audio/', views.convert_to_audio, name='convert_to_audio'),
  
  ]