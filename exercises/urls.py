from django.urls import path
from exercises import views

urlpatterns = [
    path("<int:pk>/", views.EserciziDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", views.EserciziUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", views.EserciziDeleteView.as_view(), name="article_delete"),
    path("new/", views.new_workout, name="article_new"),
    path("user", views.EserciziListViewUser.as_view(), name="article_list_user"),
    path("myworkout/", views.my_workout, name="my_workout"),
    path("exdone/", views.ex_done, name="ex_done")
]

