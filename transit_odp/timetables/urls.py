from django.urls import include, path

from transit_odp.data_quality.views.report import DraftReportOverviewView
from transit_odp.publish.views import timetable
from transit_odp.timetables.views import (
    PublishRevisionView,
    ReviewViolationsCSVFileView,
    RevisionPublishSuccessView,
    TimetableUploadModify,
    UpdateRevisionPublishView,
)
from transit_odp.timetables.views.pti import PublishedViolationsCSVFileView

urlpatterns = [
    path("", view=timetable.PublishView.as_view(), name="feed-list"),
    path("new", view=timetable.FeedUploadWizard.as_view(), name="feed-new"),
    # All these routes must restrict access to organisation who owns
    # the feed
    path(
        "<int:pk>/",
        include(
            [
                path("", view=timetable.FeedDetailView.as_view(), name="feed-detail"),
                path(
                    "violations-csv",
                    view=PublishedViolationsCSVFileView.as_view(),
                    name="revision-pti-csv",
                ),
                path(
                    "review/",
                    include(
                        [
                            path(
                                "",
                                view=PublishRevisionView.as_view(),
                                name="revision-publish",
                            ),
                            path(
                                "update",
                                view=TimetableUploadModify.as_view(),
                                name="upload-modify",
                            ),
                            path(
                                "pti-csv",
                                view=ReviewViolationsCSVFileView.as_view(),
                                name="review-pti-csv",
                            ),
                        ]
                    ),
                ),
                path(
                    "dataset-edit/",
                    view=timetable.EditLiveRevisionDescriptionView.as_view(),
                    name="dataset-edit",
                ),
                path(
                    "revision-edit/",
                    view=timetable.EditDraftRevisionDescriptionView.as_view(),
                    name="revision-edit",
                ),
                path(
                    "delete/",
                    view=timetable.RevisionDeleteTimetableView.as_view(),
                    name="revision-delete",
                ),
                path(
                    "progress/",
                    view=timetable.PublishProgressView.get_progress,
                    name="progress",
                ),
                path(
                    "success/",
                    view=RevisionPublishSuccessView.as_view(),
                    name="revision-publish-success",
                ),
                path(
                    "update/",
                    include(
                        [
                            path(
                                "",
                                view=timetable.FeedUpdateWizard.as_view(),
                                name="feed-update",
                            ),
                            path(
                                "review/",
                                include(
                                    [
                                        path(
                                            "",
                                            view=UpdateRevisionPublishView.as_view(),
                                            name="revision-update-publish",
                                        ),
                                        path(
                                            "update",
                                            view=timetable.DatasetUpdateModify.as_view(),  # noqa: E501
                                            name="update-modify",
                                        ),
                                    ]
                                ),
                            ),
                            path(
                                "success/",
                                view=timetable.RevisionUpdateSuccessView.as_view(),
                                name="revision-update-success",
                            ),
                        ]
                    ),
                ),
                path(
                    "download/",
                    view=timetable.DatasetDownloadView.as_view(),
                    name="feed-download",
                ),
                path(
                    "deactivate/",
                    include(
                        [
                            path(
                                "",
                                view=timetable.TimetableFeedArchiveView.as_view(),
                                name="feed-archive",
                            ),
                            path(
                                "success",
                                view=timetable.TimetableFeedArchiveSuccessView.as_view(),  # noqa: E501
                                name="feed-archive-success",
                            ),
                        ]
                    ),
                ),
                path(
                    "changelog/",
                    view=timetable.FeedChangeLogView.as_view(),
                    name="feed-changelog",
                ),
                path(
                    "draft-exists/",
                    view=timetable.DraftExistsView.as_view(),
                    name="feed-draft-exists",
                ),
                path(
                    "report/<int:report_id>/",
                    # TODO: use namespace?
                    include("config.urls.data_quality"),
                ),
                path(
                    "report/draft/",
                    view=DraftReportOverviewView.as_view(),
                    name="dq-draft-report",
                ),
            ]
        ),
    ),
    path(
        "delete-success",
        view=timetable.RevisionDeleteSuccessView.as_view(),
        name="revision-delete-success",
    ),
]
