# DRMBook

You need some supporting software in Ubuntu. This is probably not a complete list, but at least you need:

	apt-get install python-virtualenv python-dev libxslt1-dev libxml2-dev build-essential
	ln -s /usr/include/libxml2/libxml/ /usr/include/libxml

Now create the virtualenv and install stuff:

	virtualenv create ~/drm_python
	source ~/drm_python/bin/activate
	pip install -r drm.reqs

Now run the server:

	python server.py 31337

The client then runs as:

	python client.py localhost 31337 "my book"

A book's hash can be verified by doing:

	echo -n "This is our secret watermark for THE_BOOK_TITLE" | md5sum
