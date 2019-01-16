# These are a few helper functions for the main application

from flask import render_template


def test(test_str):
	return render_template("test.html", Test = test_str)
