from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	# Templates
	url(r'^index', 'dB_Model.views.index', name='index'),
	# url(r'^find/findP/(?P<id_empresa>\d+)', 'dB_Model.views.personas_empresa', name='personas_empresa'),
	# url(r'^find/findDP/(?P<id_persona>\d+)', 'dB_Model.views.detalle_persona', name='detalle_persona'),
	url(r'^loadOC/', 'dB_Model.views.frmLoadOC', name='frmLoadOC'),
	url(r'^readOC/', 'dB_Model.views.readFileOC', name='readFileOC'),
	url(r'^catalmacenes/', 'dB_Model.views.frm_almacenes', name='frm_almacenes'),
	url(r'^saveAlma/', 'dB_Model.views.save_almacen', name='save_almacen'),
	url(r'^catproductos/', 'dB_Model.views.frm_productos', name='frm_productos'),
	url(r'^saveProd/', 'dB_Model.views.save_producto', name='save_producto'),
	url(r'^inventario/', 'dB_Model.views.frm_inventario', name='frm_inventario'),
	url(r'^alma_inv/', 'dB_Model.views.almacen_inventario', name='almacen_inventario'),
	url(r'^loadRM/', 'dB_Model.views.loadRecMerca', name='loadRecMerca'),
	url(r'^readRM/', 'dB_Model.views.readFileRM', name='readFileRM'),
	
)