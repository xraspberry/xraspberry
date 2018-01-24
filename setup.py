from xraspberry import __version__
from setuptools import setup

setup(name='xraspberry',
      version=__version__,
      description='x-raspberry',
      packages=['xraspberry'],
      install_requires=[
            "fire",
            "alembic"
      ],
      zip_safe=False)
