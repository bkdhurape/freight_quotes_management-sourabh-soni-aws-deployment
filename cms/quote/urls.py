from django.urls import path
from quote.api.v1.additional_details_view import AdditionalDetailsView
from quote.api.v1.cargo_details_view import CargoDetailsView
from quote.api.v1.package_details_view import PackageDetailsView, PackageDetailsIdView
from quote.api.v1.quote_view import QuoteView, QuoteDetailView,QuoteListView,QuoteListingUpdate

urlpatterns = [
    path('', QuoteView.as_view()),
    path('<int:quote_id>/', QuoteDetailView.as_view()),
    path('manage_quote/',QuoteListView.as_view()),
    path('manage_quote/<int:quote_id>/',QuoteListingUpdate.as_view()),
   
    path('<int:quote_id>/package_details/', PackageDetailsView.as_view()),
    path('<int:quote_id>/cargo_details/', CargoDetailsView.as_view()),
    path('<int:quote_id>/package_details/<int:package_details_id>/',PackageDetailsIdView.as_view()),
    path('<int:quote_id>/additional_details/', AdditionalDetailsView.as_view()),
]
