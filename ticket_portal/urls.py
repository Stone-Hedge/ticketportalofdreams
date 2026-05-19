from django.urls import path
from portal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('healthz/', views.healthcheck, name='healthcheck'),
    path('robots.txt', views.robots, name='robots'),
    path('passcode/', views.passcode_view, name='passcode'),
    path('choose-person/', views.choose_person, name='choose_person'),
    path('change-person/', views.change_person, name='change_person'),
    path('fixtures/', views.fixtures_board, name='fixtures'),
    path('manage-data/', views.manage_data, name='manage_data'),
    path('fixtures/<int:fixture_id>/', views.fixture_detail, name='fixture_detail'),
    path('allocation/<int:allocation_id>/edit/', views.edit_allocation, name='edit_allocation'),
    path('allocation/<int:allocation_id>/update/', views.update_allocation, name='update_allocation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/available/', views.dashboard_available, name='dashboard_available'),
    path('dashboard/unpaid/', views.dashboard_unpaid, name='dashboard_unpaid'),
    path('dashboard/transfers/', views.dashboard_transfers, name='dashboard_transfers'),
    path('dashboard/fairness/', views.dashboard_fairness, name='dashboard_fairness'),
    path('audit/', views.audit_log, name='audit_log'),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-portal/import/', views.admin_import, name='admin_import'),
    path('admin-portal/export/', views.admin_export, name='admin_export'),
]
