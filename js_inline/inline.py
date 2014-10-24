import os
import re
import argparse


argumentsParser = argparse.ArgumentParser(description='JS to HTML inliner')
argumentsParser.add_argument("-i", "--input")
arguments = argumentsParser.parse_args();


with open(arguments.input, 'rb') as html_hdl:
	html = html_hdl.read()

scripts = []
matches = re.finditer(r'<script[^>]+src\s*=\s*"([^"]+)"[^>]*>.*?</script>', html)
for match in matches:
	scripts.append({
		'start': match.span()[0],
		'end': match.span()[1],
		'fileName': match.group(1)
	})

for script in reversed(scripts):
	if ("http" in script['fileName']):
		continue

	with open(script['fileName']) as js_hdl:
		html = html[:script['start']] + '<script>' + js_hdl.read() + '</script>' + html[script['end']:]


print html
