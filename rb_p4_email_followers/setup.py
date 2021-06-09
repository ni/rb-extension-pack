from __future__ import unicode_literals

from setuptools import find_packages
from reviewboard.extensions.packaging import setup


setup(
    name="rb_p4_email_followers",
    version="0.1.1",
    description="Extension for Review Board to email p4 reviews when a review is posted",
    author="Kristen Jaimes",
    author_email="kristen.jaimes@ni.com",
    maintainer="Dawn Thomas",
    maintainer_email="dawn.thomas@ni.com",
    packages=find_packages(),
    entry_points={
        "reviewboard.extensions": [
            "rb_p4_email_followers = rb_p4_email_followers.extension:FollowersEmailExtension"
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Review Board",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
