from mysite.urls import path
from .views import IndexView, DetailView, ReseultView, vote

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', ReseultView.as_view(), name='results'),
    path('<int:question_id>/vote/', vote, name='vote')


]