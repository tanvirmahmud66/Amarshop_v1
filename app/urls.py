from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (

    AdminCreateView,
    AdminLoginView,
    AdminLogoutView,

    ProfileView,
    ProfilePictureChangeView,
    ProfilePictureRemoveView,
    ProfileUpdateView,

    DashboardView,

    SalesListView,
    SaleDetailsView,
    ClientUserView,
    InvoiceListView,
    InvoiceAddItem,
    get_filtered_products,
    InvoiceRemoveItem,
    SalesPayment,

    InventoryListView,
    InventoryDetailsView,
    InventoryPriceSet,
    InventoryUpdateView,
    InventoryDeleteView,

    PurchaseListView,
    PurchaseCreateView,
    PurchaseDetailsView,
    PurchaseUpdateView,
    PurchaseDeleteView,

    ProductListView,
    CreateProductView,
    ProductDetailsView,
    ProductUpdateView,
    ProductDeleteView,

    CreateCategoryView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,

    CreateBrandView,
    BrandListView,
    BrandUpdateView,
    BrandDeleteView,

    SuppliersListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,

    ReportView,

    OrderView,

    StoreManageView,
)

urlpatterns = [

    path('',AdminLoginView.as_view(),name='admin-login'),
    path('signup/',AdminCreateView.as_view(),name='admin-signup'),
    path('logout/', AdminLogoutView.as_view(), name='admin-logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    
    path('profile/<int:pk>/',ProfileView.as_view(),name='profile'),
    path('profile/<int:pk>/change-picture/',ProfilePictureChangeView.as_view(),name='profile-change-picture'),
    path('profile/<int:pk>/remove-picture/',ProfilePictureRemoveView.as_view(),name='profile-picture-remove'),
    path('profile/<int:pk>/update-profile/',ProfileUpdateView.as_view(),name='profile-update'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('sales/',SalesListView.as_view(),name='sales-list'),
    path('sales/new-sale/',ClientUserView.as_view(),name='new-sale'),
    path('sales/<int:pk>/sale-details/',SaleDetailsView.as_view(),name='sale-details'),
    path('sales/new-sale/<str:pk>/invoice/', InvoiceListView.as_view(),name='invoice-list'),
    path('sales/new-sale/<str:pk>/invoice/add-item/',InvoiceAddItem.as_view(),name='invoice-add-item'),
    path('get_filtered_products/', get_filtered_products, name='get_filtered_products'),
    path('sales/new-sale/<str:email>/invoice/<int:pk>/remove-item/',InvoiceRemoveItem.as_view(),name='invoice-remove-item'),
    path('sales/new-sale/<str:pk>/payment/',SalesPayment.as_view(),name='sales-payment'),

    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/details/',InventoryDetailsView.as_view(),name='inventory-details'),
    path('inventory/<int:pk>/set-price/',InventoryPriceSet.as_view(),name='inventory-setPrice'),
    path('inventory/<int:pk>/update/',InventoryUpdateView.as_view(),name='inventory-update'),
    path('inventory/<int:pk>/delete/',InventoryDeleteView.as_view(),name='inventory-delete'),

    path('purchase/', PurchaseListView.as_view(),name='purchase-list'),
    path('purchase/new-purchase/',PurchaseCreateView.as_view(),name='new-purchase'),
    path('purchase/<int:pk>/details/',PurchaseDetailsView.as_view(),name='purchase-details'),
    path('purchase/<int:pk>/update/',PurchaseUpdateView.as_view(),name='purchase-update'),
    path('purchase/<int:pk>/delete/',PurchaseDeleteView.as_view(),name='purchase-delete'),

    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/create-product/', CreateProductView.as_view(), name='create-product'),
    path('product/<int:pk>/details/', ProductDetailsView.as_view(), name='product-details'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/',ProductDeleteView.as_view(), name='product-delete'),

    path('category/',CategoryListView.as_view(),name='category-list'),
    path('category/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('category/<int:pk>/update/',CategoryUpdateView.as_view(),name='category-update'),
    path('category/<int:pk>/delete/',CategoryDeleteView.as_view(),name='category-delete'),

    path('brand/', BrandListView.as_view(), name='brand-list'),
    path('brand/create-brand/', CreateBrandView.as_view(), name='create-brand'),
    path('brand/<int:pk>/update/', BrandUpdateView.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete', BrandDeleteView.as_view(), name='brand-delete'),


    path('reports/', ReportView.as_view(), name='reports'),


    path('suppliers/', SuppliersListView.as_view(), name='supplier-list'),
    path('suppliers/create-supplier/',SupplierCreateView.as_view(), name='create-supplier'),
    path('suppliers/supplier/<int:pk>/update/',SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/supplier/<int:pk>/delete/',SupplierDeleteView.as_view(), name='supplier-delete'),


    path('orders/', OrderView.as_view(), name='orders'),


    path('manage-store/', StoreManageView.as_view(), name='manage'),

]



