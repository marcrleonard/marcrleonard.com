import datetime
import os
from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
import pathlib
import shutil
import pygments

# example environ output from cloudflare
# {
# 	'SHELL': '/bin/bash',
# 	'PIPENV_VENV_IN_PROJECT': '1',
# 	'NVM_INC': '/opt/buildhome/.nvm/versions/node/v12.18.0/include/node',
# 	'SUDO_GID': '0', 'rvm_delete_flag': '0', 'rvm_prefix': '/opt/buildhome', 'PYTHON_VERSION': '3.7',
# 	'LANGUAGE': 'en_US:en', 'NODE_OPTIONS': '--max_old_space_size=4096', 'ELM_VERSION': '0.19.0-bugfix6',
# 	'HUGO_VERSION': '0.54.0', 'REPO_DIR': '/opt/buildhome/repo',
# 	'MY_RUBY_HOME': '/opt/buildhome/.rvm/rubies/ruby-2.7.1', 'SUDO_COMMAND': '/opt/build/bin/build python3 main.py',
# 	'GIMME_NO_ENV_ALIAS': 'true', 'YARN_VERSION': '1.22.4', 'SUDO_USER': 'root', 'install_flag': '1',
# 	'RUBY_VERSION': 'ruby-2.7.1', 'NVM_VERSION': '0.35.3', 'PWD': '/opt/buildhome/repo', 'LOGNAME': 'buildbot',
# 	'rvm_version': '1.29.12 (latest)', 'GIMME_CGO_ENABLED': 'true', 'NF_IMAGE_TAG': 'latest', 'HOME': '/opt/buildhome',
# 	'LANG': 'en_US.UTF-8', 'VIRTUAL_ENV': '/opt/buildhome/python3.7', 'LZ4_VERSION': '1.8.0',
# 	'GOROOT': '/opt/buildhome/.gimme/versions/go1.14.4.linux.amd64', 'BINRC_VERSION': '0.2.9', 'GIMME_TYPE': 'binary',
# 	'NVM_DIR': '/opt/buildhome/.nvm', 'NETLIFY': 'true', 'rvm_bin_path': '/opt/buildhome/.rvm/bin',
# 	'GEM_PATH': '/opt/buildhome/.rvm/gems/ruby-2.7.1:/opt/buildhome/.rvm/gems/ruby-2.7.1@global',
# 	'GIMME_ENV_PREFIX': '/opt/buildhome/.gimme/env', 'GEM_HOME': '/opt/buildhome/.rvm/gems/ruby-2.7.1',
# 	'CUSTOM_SWIFT': '0', 'TERM': 'unknown', 'CF_PAGES': '1', 'USER': 'buildbot', 'RVM_DIR': '/opt/buildhome/.rvm',
# 	'SHLVL': '2', 'NVM_CD_FLAGS': '', 'GIMME_GO_VERSION': '1.14.4', 'rvm_ruby_string': 'ruby-2.7.1',
# 	'PANDOC_VERSION': '2.4', 'GOCACHE': '/opt/buildhome/.gimme_cache/gocache', 'PIPENV_DEFAULT_PYTHON_VERSION': '2.7',
# 	'CF_PAGES_URL': 'https://266b9b5a.portfolio-site-d6m.pages.dev', 'SWIFTENV_ROOT': '/opt/buildhome/.swiftenv',
# 	'PS1': '(python3.7) ', 'LC_ALL': 'en_US.UTF-8', 'CF_PAGES_COMMIT_SHA': '18e8fd0b206be29c46f72c06ca8116986e10a7f6',
# 	'PIPENV_RUNTIME': '2.7',
# 	'PATH': '/opt/buildhome/.wasmer/bin:/opt/buildhome/.gimme/versions/go1.14.4.linux.amd64/bin:/opt/buildhome/cache/.binrc-a5679f71f5966d1b3450c8dcd52d4743ec08e632/binaries/gohugoio/hugo/v0.54.0:/opt/buildhome/.rvm/gems/ruby-2.7.1/bin:/opt/buildhome/.rvm/gems/ruby-2.7.1@global/bin:/opt/buildhome/.rvm/rubies/ruby-2.7.1/bin:/opt/buildhome/.rvm/bin:/opt/buildhome/.nvm/versions/node/v12.18.0/bin:/opt/buildhome/python3.7/bin:/opt/buildhome/.asdf/shims:/opt/buildhome/.asdf/bin:/opt/buildhome/.swiftenv/bin:/opt/buildhome/.swiftenv/shims:/opt/buildhome/.php:/opt/buildhome/.binrc/bin:/usr/local/rvm/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/buildhome/.cask/bin:/opt/buildhome/.gimme/bin:/opt/buildhome/.dotnet/tools:/opt/buildhome/.dotnet:/opt/buildhome/.local/bin',
# 	'ROOT_DIR': '/', 'SUDO_UID': '0', 'CF_PAGES_BRANCH': 'master', 'NF_IMAGE_VERSION': 'latest',
# 	'NETLIFY_NODE_VERSION': '12.18.0', 'NVM_BIN': '/opt/buildhome/.nvm/versions/node/v12.18.0/bin',
# 	'NODE_VERSION': 'v12.18.0', 'WASMER_CACHE_DIR': '/opt/buildhome/.wasmer/cache',
# 	'IRBRC': '/opt/buildhome/.rvm/rubies/ruby-2.7.1/.irbrc', 'rvm_path': '/opt/buildhome/.rvm',
# 	'WASMER_DIR': '/opt/buildhome/.wasmer', 'OLDPWD': '/opt/buildhome', 'GOPATH': '/opt/buildhome/.gimme_cache/gopath',
# 	'JAVA_VERSION': 'default_sdk', '_': '/opt/buildhome/python3.7/bin/python3'
# }

cloud_build = str(os.environ.get('CF_PAGES')) == "1"
# cloud_build = True

print(os.environ)

print(f"Cloud Build: {cloud_build}")

full_url = "http://localhost:63342/developer-portfolio-site/build"
# full_url = "/"
if cloud_build:
	full_url = os.environ.get("CF_PAGES_URL")
	if os.environ.get("CF_PAGES_BRANCH") == "master":
		# if this isn't set, full_url will be the 'internal' url
		full_url = "https://marcrleonard.com"

NEWS_ITEMS = [
	# {
	# 	'thumbnail': 'img/thumbs/4-3.jpg',
	# 	'full_image': 'img/news/1.jpg',
	# 	'title': 'Django Is Awesome.',
	# 	'date': 'January 3, 2022',
	# 	'category': 'Python',
	# 	'text': [
	# 		"Django is awesome.",
	# 		"That is all."
	# 	],
	# }
]

from pelican.readers import MarkdownReader
from pelican.tests.support import get_settings

BUILD_FOLDER = 'build'
SOURCE_FOLDER = 'source'

# Make main pages in the nav
# the order of this is the order
# the items show up in the nav
pages_nav = [
	# url, title, html file
	("/", "home", "pages/home.html"),
	("/about", "about", "pages/about.html"),
	("/experience", "experience", "pages/experience.html"),
	("/odds-ends", "odds & ends", "pages/ponderings.html"),
]

# these are pages that are not in the nav but exist
addl_pages = [
	# url, title, html file
	("/resume", "_", "pages/resume.html"),
]


env = Environment(
	loader=PackageLoader(SOURCE_FOLDER, '_templates'),
	# loader = FileSystemLoader(t_path),
	autoescape=select_autoescape()
)
os.makedirs(BUILD_FOLDER, exist_ok=True)

md = MarkdownReader(settings=get_settings(), )

# Make blog pages
blog_dir = "source/blog"
for file in os.listdir("source/blog"):

	if str(file).startswith("_"):
		continue

	html_text, metadata = md.read(f"{blog_dir}/{file}")

	# html_text = html_text.replace("<code>", "<code class='highlight'>")

	post_date = datetime.datetime.fromisoformat(metadata['date'].isoformat())

	title = metadata['title']
	default_slug = title.lower().replace(" ", "-")
	slug = metadata.get('slug', default_slug)

	url = f'{post_date.year}/{post_date.month}/{slug}'

	cats = [str(c).lstrip().rstrip().lower() for c in str(metadata['category']).split(",")]

	news_item = {
		'thumbnail': 'img/thumbs/4-3.jpg',
		'full_image': 'img/news/1.jpg',
		'title': title,
		'date': post_date,
		'category': cats,
		'tags': metadata['tags'],
		'slug': url,
		'summary': metadata['summary'],
		'text': html_text,
	}

	blog_location = f"{BUILD_FOLDER}/blog/{url}"
	os.makedirs(blog_location, exist_ok=True)

	with open(f'{blog_location}/index.html', 'w') as f:
		f.write(env.get_template('_blog.html').render({
			"full_url": full_url,
			'news_item': news_item,
			"fixed_footer": True,
			"nav_items": pages_nav,
			"page_slug": url
		}))

	NEWS_ITEMS.append(news_item)

NEWS_ITEMS.sort(key = lambda x:x['date'])
NEWS_ITEMS.reverse()

# Create rss
with open(f'{BUILD_FOLDER}/rss.xml', 'w') as f:
	f.write(env.get_template('rss.xml').render({
		'news_items': NEWS_ITEMS,
		'build_date': datetime.datetime.now(),
		'full_url': full_url,
	}))

from collections import defaultdict
news_items_by_year = defaultdict(list)
for i in NEWS_ITEMS:
	date = i['date']
	news_items_by_year[str(date.year)].append(i)

import letterboxd

movies_by_year = letterboxd.get_watched_films_from_rss()

# render all pages. some are nav pages and some are not in the nav
all_pages = pages_nav.copy()
all_pages.extend(addl_pages)
for url, title, html_file in all_pages:
	output_location = f"{BUILD_FOLDER}{url}"
	os.makedirs(output_location, exist_ok=True)
	with open(f'{output_location}/index.html', 'w') as f:
		f.write(env.get_template(html_file).render({
			"nav_items": pages_nav,
			"page_slug": url, # used to determine if the nav link should be active or not
			'full_url': full_url,
			"fixed_footer": True,
			'news_items': NEWS_ITEMS,
			"news_items_by_year": news_items_by_year,
			"movies_by_year": movies_by_year
		}))


folders_to_copy = [
	(f'{SOURCE_FOLDER}/css/', f'{BUILD_FOLDER}/css/'),
	(f'{SOURCE_FOLDER}/img/', f'{BUILD_FOLDER}/img/'),
	(f'{SOURCE_FOLDER}/js/', f'{BUILD_FOLDER}/js/'),
	(f'{SOURCE_FOLDER}/assets/', f'{BUILD_FOLDER}/assets/'),

]


def recursivly_copy_folders(source_dir, target_dir):
	if not pathlib.Path(source_dir).exists():
		return

	file_names = os.listdir(source_dir)

	os.makedirs(target_dir, exist_ok=True)

	for file_name in file_names:

		original_file = pathlib.Path(source_dir, file_name)

		new_path = pathlib.Path(target_dir, file_name)

		if original_file.is_file():
			shutil.copy2(original_file, new_path)
		else:
			os.makedirs(new_path, exist_ok=True)

			recursivly_copy_folders(original_file, new_path)


for source_dir, target_dir in folders_to_copy:
	recursivly_copy_folders(source_dir, target_dir)

# copy ico
shutil.copy2(f'{SOURCE_FOLDER}/img/favicon.ico', f'{BUILD_FOLDER}/')