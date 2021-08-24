import json
import requests

from .constants import SWAPI_URL, CATEGORY_ID_MAP
from .models import Customization


def fetch_data(category: str, item_id: int=None) -> list:
	""" 

	Accepts a category name and optionally item_id,
	fetches the data from SWAPI
	and returns the relevant data

	"""

	fetch = True
	results = []
	url = SWAPI_URL + category
	if item_id:
		url += '/%s/' % str(item_id)

	while fetch:
		res = json.loads(requests.get(url).content)

		if item_id:
			return [res]

		results += res.get("results", [])
		# fetch flag determines if additional records are to be fetched
		fetch = url = res.get("next")

	return results


def get_customization(user_id: int, category: str, search_key: str) -> dict:
	"""

	Returns {item_id: (custom_name, is_favorite), ...} mapping
	for the given category for a user

	"""

	if not user_id:
		return {}

	table = Customization.objects.filter(
		user_id=user_id,
		category=CATEGORY_ID_MAP.get(category)
	)

	if search_key:
		table.filter(name__icontains=search_key)

	custom_map = {}
	for row in table.values_list("item_id", "name", "is_favorite"):
		custom_map[row[0]] = (row[1], row[2])

	return custom_map

def add_additional_fields(item_dict, item, category):
    item_dict["created"] = item.get("created")
    item_dict["updated"] = item.get("edited")
    item_dict["url"] = item.get("url")

    if category == "films":
        item_dict["relased_at"] = item.get("released_at")

    return item_dict
