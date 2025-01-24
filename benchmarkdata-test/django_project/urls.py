from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    DefaultFormByFieldView,
    DefaultFormsetView,
    DefaultFormView,
    FormHorizontalView,
    FormInlineView,
    FormWithFilesView,
    HomePageView,
    MiscView,
    PaginationView,
    AnalyticsView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("formset", DefaultFormsetView.as_view(), name="formset_default"),
    path("form", DefaultFormView.as_view(), name="form_default"),
    path("form_by_field", DefaultFormByFieldView.as_view(), name="form_by_field"),
    path("form_horizontal", FormHorizontalView.as_view(), name="form_horizontal"),
    path("form_inline", FormInlineView.as_view(), name="form_inline"),
    path("form_with_files", FormWithFilesView.as_view(), name="form_with_files"),
    path("pagination", PaginationView.as_view(), name="pagination"),
    path("misc", MiscView.as_view(), name="misc"),
    path('analytics-viewall', AnalyticsView.as_view(), name='analytics_viewall'),  # Correct the URL pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)