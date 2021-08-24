from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from favorites.views import CommonView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('planets/<item_id>/', CommonView.as_view(), {"category": "planets"}),
    path('planets/', CommonView.as_view(), {"category": "planets"}),
    path('films/<item_id>/', CommonView.as_view(), {"category": "films"}),
    path('films/', CommonView.as_view(), {"category": "films"}),
    path('people/<item_id>/', CommonView.as_view(), {"category": "people"}),
    path('people/', CommonView.as_view(), {"category": "people"}),
    path('starships/<item_id>/', CommonView.as_view(), {"category": "starships"}),
    path('starships/', CommonView.as_view(), {"category": "starships"}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns+=[
        path('__debug__/', include(debug_toolbar.urls))
    ]
