Email Followers
===============

This extension adds additional recipients to the email notification when a review is published, without adding them to the review as "groups" or "people". We call these recipients "followers". Followers can configure which paths they follow using their `p4 user` specification's Reviews field.

This functionality allows users to self-service notification configuration when changes are being proposed in paths they care about.

Requirements
------------
This extension has been tested with Review Board 2.5.x. Only Perforce repositories are supported (since that's how followers configure the paths to follow).