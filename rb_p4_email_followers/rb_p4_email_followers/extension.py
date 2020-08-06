from django.contrib.auth.models import User

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestPublishedEmailHook


def _get_followers(review_request):
    """Return a list of all `User`s who have configured `p4 reviews` for the files in this review request."""
    all_reviewers = []
    repository = review_request.repository
    if repository is None:
        return []
    scmtool = repository.get_scmtool()
    if scmtool.name == "Perforce":
        client = scmtool.client
        with client.run_worker():
            diffset = review_request.get_latest_diffset()
            if diffset is None:
                return []
            diff_files_mgr = diffset.files
            diff_files = (
                diff_files_mgr.all()
            )  # get actual FileDiffs from Django RelatedManager
            p4_paths = _get_unique_paths(diff_files)
            for p4_path in p4_paths:
                # possible optimization: make this one call to p4 reviews with a lot of arguments (think about command line length etc.)
                all_reviewers.extend(client.p4.run_reviews(p4_path))

    followers = _get_users_from_reviewers(all_reviewers, review_request)
    return followers


def _get_unique_paths(diff_files):
    """Get filenames from the FileDiffs, including both names for renamed/moved files."""
    paths = set()

    for diff_file in diff_files:
        paths.add(diff_file.source_file)
        paths.add(diff_file.dest_file)

    return paths


def _get_users_from_reviewers(reviewers, review_request):
    """Turn output from `p4 reviews` into a list of Django User objects."""
    # Reviews returns something like [{'user': 'scot', 'name': 'Scot Salmon', 'email': 'scot.salmon@ni.com'}].
    # We could look up the user and/or email in the review-board User database, but not all the p4 users are
    # in that database, and we might want to notify them anyway. To ensure a unique id that won't conflict
    # with actual User entries, we'll just use a negative id.
    emails = set(reviewer["email"] for reviewer in reviewers)
    dummy_users = [
        User(email=email, id=-(index + 1)) for index, email in enumerate(emails)
    ]
    return dummy_users


class FollowersEmailHook(ReviewRequestPublishedEmailHook):
    """Add anyone mentioned in `p4 reviews` for path under review to the email notification."""

    def get_cc_field(self, cc_field, review_request, user):
        followers = _get_followers(review_request)
        cc_field.update(followers)
        return cc_field


class FollowersEmailExtension(Extension):
    def initialize(self):
        FollowersEmailHook(self)
