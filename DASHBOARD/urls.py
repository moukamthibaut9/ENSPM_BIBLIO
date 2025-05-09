from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard' ),
    path('departments',views.departments, name='departments' ),
    path('statut_verification',views.statut_verification, name='statut_verification' ),
    path('specialities/<int:speciality_id>',views.specialities, name='specialities' ),
    path('doc_submit',views.DocSubmit.as_view(),name='doc_submit' ),
    path('doc_update/<int:pk>',views.DocUpdate.as_view(),name='doc_update' ),
    path('doc_delete/<int:pk>',views.DocDelete.as_view(),name='doc_delete' ),
    path('plagiat_evaluation/<int:book_1_id>',views.plagiat_evaluation,name='plagiat_evaluation'),
    path('search',views.search,name='search' ),
    path('specialities/<int:speciality_id>/book/<int:book_id>',views.pdf_download,name='pdf_download' ),
]