# clean the following modules using `make`
# or run with additional modules using `make more="temporary.py"`

modules = \
	fieldclimate \
	tests \
	${more}

clean:
	isort -rc -m 3 -w 88 -tc $(modules)
	black --py36 --skip-numeric-underscore-normalization $(modules)
