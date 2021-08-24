from django.http import HttpResponse
from rest_framework.views import APIView

from .models import Customization
from .constants import CATEGORY_ID_MAP
from .utilities import fetch_data, get_customization


class CommonView(APIView):

    def get(self, request, category, item_id=None):
        """
        Display a list of `<category>` (plantes / films / people/ starships)
        from swapi API with is_favorite flag and custom_name, if any
        Optionally performs search on name and return details of item_id alone

        :params
             - `search_key`: <str>, <optional>
             - `category`: <str>, <required>
             - `item_id`: <str>, <optional>

        """

        response = []
        user_id = request.GET.get("user_id", None)
        search_key = request.GET.get("search_key", "")
        data = fetch_data(category, item_id)
        custom_map = get_customization(user_id, category, search_key)

        for item in data:
            name, is_favorite = custom_map.get(
                int(item.get("url").split("/")[-2]),
                (item.get("name"), False)
            )

            if search_key and search_key not in name:
                continue

            response.append({
                "name": name,
                "created": item.get("created"),
                "updated": item.get("edited"),
                "url": item.get("url"),
                "is_favorite": is_favorite,
            })

        return HttpResponse(response)

    def post(self, request, category, item_id):
        """ To add an item (plantes / films / people/ starships) as favorite
        and allow setting a custom title/name to an item

        :params
            - `user_id`: <int>, <required>
            - `item_id`: <int>, <required>
            - `name`: <str>, <optional>
            - `category`: <str>, <required>
            - `is_favorite`: <str>, <optional>

        """
        data = request.data
        user_id = data.get("user_id")
        name = data.get("name", "")

        custom_obj, _ = Customization.objects.get_or_create(
            user_id=user_id, item_id=item_id, category=CATEGORY_ID_MAP.get(category)
        )

        if "is_favorite" in data:
            custom_obj.is_favorite = data.get("is_favorite")
        if name:
            custom_obj.name = name

        custom_obj.save()

        return HttpResponse("success")