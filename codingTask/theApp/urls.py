from django.urls import path
from .views.login import login_view, logout_view
from .views.signup import signup_view
from .views.spam import report_spam_view, get_all_spam_view
from .views.search import search_by_name_view, search_by_number_view

urlpatterns = [

    path('signup/', signup_view, name = 'signup'),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    
    path('spam/report/', report_spam_view, name = 'report_spam'),
    path('spam/view/all/', get_all_spam_view),

    path('search/byName/', search_by_name_view, name = 'search_by_name'),
    path('search/byNumber/', search_by_number_view, name = 'search_by_number'),

]