import py7digital

def test_get_artist_detail_returns_keane():
	artists = py7digital.get_artist_detail('1')
	for artist in artists.get_next_page():
		assert artist.get_name().lower() == "keane"

def test_artist_search_returns_names_containing_stone():
	artists = py7digital.search_artist("stones")
	for i in artists.get_next_page():
		assert i.get_name().lower().find("stones") > -1