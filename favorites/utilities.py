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

	next = True
	results = []
	url = SWAPI_URL + category
	if item_id:
		url += '/%s/' % str(item_id)

	while next:
		res = json.loads(requests.get(url).content)
		if item_id:
			return [res]
		results += res.get("results", [])
		next = url = res.get("next")

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




