from transit_odp.changelog.constants import ConsumerIssue, PublisherIssue
from transit_odp.changelog.managers import (
    ConsumerKnownIssueManager,
    PublisherKnownIssueManager,
)
from transit_odp.changelog.models import KnownIssues


class ConsumerKnownIssues(KnownIssues):
    class Meta:
        proxy = True
        verbose_name = "Consumer Known Issues"
        verbose_name_plural = "Consumer Known Issues"

    objects = ConsumerKnownIssueManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, category=ConsumerIssue, **kwargs)


class PublisherKnownIssues(KnownIssues):
    class Meta:
        proxy = True
        verbose_name = "Publisher Known Issues"
        verbose_name_plural = "Publisher Known Issues"

    objects = PublisherKnownIssueManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, category=PublisherIssue, **kwargs)
