from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all_categories/$', views.all_categories, name='all_categories'),
    url(r'^create_category/$', views.create_category, name='create_category'),
    url(r'^add_expense/$', views.add_expense, name='add_expense'),
    url(r'^all_expenses/$', views.all_expenses, name='all_expenses'),
    url(r'^report/$', views.report, name='report'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]