import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='www',
      version='0.0',
      description='Webinterface for the Wetterfrosch project.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Bernhard Essl',
      author_email='bernhardessl@gmail.com',
      url='https://github.com/bessl/Wetterfrosch',
      keywords='web pyramid weather weatherstation',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='www',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = www:main
      [console_scripts]
      initialize_www_db = www.scripts.initializedb:main
      """,
      )
