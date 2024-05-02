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
    SalesInvoiceListView,
    ConfirmSaleView,
    get_filtered_products,
    InvoiceRemoveItem,
    SalesPayment,

    PurchaseListView,
    PurchaseLinpUpView,
    get_filtered_subcategory,
    PurchaseInvoiceEditView,
    PurchaseInvoiceDeleteView,
    PurchaseConfirmView,
    PurchaseDetailsView,
    PurchaseUpdateView,
    PurchaseDeleteView,

    ProductListView,
    CreateProductView,
    ProductDetailsView,
    ProductUpdateView,
    ProductDeleteView,

    CategoryView,
    CategoryUpdateView,
    CategoryDeleteView,
    SubcategoryView,

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
    path('sales/new-sale/invoice/',SalesInvoiceListView.as_view(),name='new-sale-invoice'),
    path('sales/new-sale/confirm-sale/',ConfirmSaleView.as_view(),name='new-sale-confirm'),
    path('sales/<int:pk>/sale-details/',SaleDetailsView.as_view(),name='sale-details'),
    path('get_filtered_products/', get_filtered_products, name='get_filtered_products'),
    path('sales/new-sale/<str:email>/invoice/<int:pk>/remove-item/',InvoiceRemoveItem.as_view(),name='invoice-remove-item'),
    path('sales/new-sale/<str:pk>/payment/',SalesPayment.as_view(),name='sales-payment'),

    path('purchase/', PurchaseListView.as_view(),name='purchase-list'),
    path('purchase/new-purchase/invoice-list',PurchaseLinpUpView.as_view(),name='new-purchase-invoice'),
    path('purchase/new-purchase/invoice-list/item-edit/<int:pk>/',PurchaseInvoiceEditView.as_view(),name='purchase-invoice-edit'),
    path('purchase/new-purchase/invoice-list/item-remove/<int:pk>/',PurchaseInvoiceDeleteView.as_view(),name='purchase-invoice-remove'),
    path('get_filtered_subcategory/', get_filtered_subcategory, name='get_filtered_subcategory'),
    path('purchase/new-purchase/purchase-confirm/',PurchaseConfirmView.as_view(),name='purchase-confirm'),
    path('purchase/<int:pk>/details/',PurchaseDetailsView.as_view(),name='purchase-details'),
    path('purchase/<int:pk>/update/',PurchaseUpdateView.as_view(),name='purchase-update'),
    path('purchase/<int:pk>/delete/',PurchaseDeleteView.as_view(),name='purchase-delete'),

    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/create-product/', CreateProductView.as_view(), name='create-product'),
    path('product/<int:pk>/details/', ProductDetailsView.as_view(), name='product-details'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/',ProductDeleteView.as_view(), name='product-delete'),

    path('category/', CategoryView.as_view(), name='category-list'),
    path('category/<int:pk>/update/',CategoryUpdateView.as_view(),name='category-update'),
    path('category/<int:pk>/delete/',CategoryDeleteView.as_view(),name='category-delete'),
    path('category/<str:pk>/',SubcategoryView.as_view(),name='sub-categories'),

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



