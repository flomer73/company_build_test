#encoding:utf-8
from django.db.models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import *
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.decorators import *
from dB_Model.models import *
import json
import xlrd
from django.core import serializers

def index(request):
	context = {}
	return render(request, 'index.html', context)

def frmLoadOC(request):
	context = {}
	return render(request, 'frm_loadFileOC.html', context)

def readFileOC(request):
	book = xlrd.open_workbook(request.POST['path'] + request.POST['name'])	
	first_sheet = book.sheet_by_index(0)
	#Valida que contenga el sub inventario y el PDV
	if first_sheet.cell(0, 0).value != 'Sub inventario':
		data = {'error': 'En el archivo falta la celda con el valor del Sub inventario'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	if first_sheet.cell(0, 1).value != 'PDV':
		data = {'error': 'En el archivo falta la celda con el valor PDV'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	for x in range(2, first_sheet.ncols - 1):
		art_ref = first_sheet.cell(0, x).value
		# verificar existencia de articulos
		articulo = cat_articulo.objects.filter(referencia = art_ref)
		if articulo.count() == 0: # add
			reg = cat_articulo (referencia = art_ref)
			reg.save()
			id_art = reg.id
		else: #existe
			id_art = articulo[0].id

		for y in range(1, first_sheet.nrows - 2):
			totalFila = first_sheet.cell(y, first_sheet.ncols - 1).value
			if totalFila > 0:
				if first_sheet.cell(y, x).value != '':
					existOC = cat_almacen.objects.filter(sub_inventario = first_sheet.cell(y, 0).value)
					if existOC.count() == 0: # si no existe add
						reg2 = cat_almacen (
							sub_inventario = first_sheet.cell(y, 0).value,
							pdv			   = first_sheet.cell(y, 1).value
						)
						reg2.save()
						id_oc = reg2.id
					else:
						id_oc = existOC[0].id

					existOCD = orden_compra_det.objects.filter(id_sub_inventario_id = id_oc, id_articulo_id = id_art).count()
					if existOCD == 0: # si no existe add
						reg3 = orden_compra_det (
							id_sub_inventario_id = id_oc,
							id_articulo_id    	 = id_art,
							cantidad	   		 = first_sheet.cell(y, x).value
						)
						reg3.save()
	
	ordenes_det = orden_compra_det.objects.filter(estatus__isnull = True)
	data 	= dict()
	row 	= dict()
	for orden_det in ordenes_det:
		row['idOC_det'] 		= orden_det.id
		row['idOC'] 			= orden_det.id_sub_inventario_id
		row['sub_inventario'] 	= orden_det.id_sub_inventario.sub_inventario
		row['pdv'] 				= orden_det.id_sub_inventario.pdv
		row['id_articulo'] 		= orden_det.id_articulo.referencia
		row['cantidad'] 		= orden_det.cantidad
		data[orden_det.id] 	= row
		row = dict()
	return HttpResponse(json.dumps(data), mimetype="application/json")	

def frm_almacenes(request):
	almacenes = cat_almacen.objects.all()
	context = {'dbAlmacenes': almacenes}
	return render(request, 'frm_almacenes.html', context)

def save_almacen(request):
	existAlmacen = cat_almacen.objects.filter(sub_inventario = request.POST['identificador'], 
		pdv = request.POST['nombre'])
	if existAlmacen.count() == 0: # add
		reg = cat_almacen (
			sub_inventario = request.POST['identificador'],
			pdv			   = request.POST['nombre']
		)
		reg.save()
		id_reg = reg.id
		respuesta = 'NUEVO'
	else:
		id_reg = existAlmacen[0].id
		respuesta = 'EXISTE'
	data = {'id': id_reg, 'estatus': respuesta}
	return HttpResponse(json.dumps(data), mimetype="application/json")

def frm_productos(request):
	articulos = cat_articulo.objects.all()
	context = {'dbArticulos': articulos}
	return render(request, 'frm_productos.html', context)

def save_producto(request):
	existProd = cat_articulo.objects.filter(referencia = request.POST['referencia'])
	if existProd.count() == 0: # add
		reg = cat_articulo (
			referencia = request.POST['referencia']
		)
		reg.save()
		id_reg = reg.id
		respuesta = 'NUEVO'
	else:
		id_reg = existProd[0].id
		respuesta = 'EXISTE'
	data = {'id': id_reg, 'estatus': respuesta}
	return HttpResponse(json.dumps(data), mimetype="application/json")

def frm_inventario(request):
	almacenes = cat_almacen.objects.all()
	context = {'dbAlmacenes': almacenes}
	return render(request, 'frm_inventario.html', context)

def almacen_inventario(request):
	listado = inventario.objects.filter(id_sub_inventario = request.POST['id_almacen'])
	data 	= dict()
	row 	= dict()
	for articulo in listado:
		row['articulo'] 	= articulo.id_articulo.referencia
		row['existencia'] 	= articulo.existencia
		data[articulo.id] 	= row
		row = dict()
	return HttpResponse(json.dumps(data), mimetype="application/json")

def loadRecMerca(request):
	ordenes_det = orden_compra_det.objects.filter(estatus__isnull = True)
	context = {'dbOrdenes_det': ordenes_det}
	return render(request, 'frm_loadFileRM.html', context)

def readFileRM(request):
	set_ord_det_id = request.POST['set_ord_det_id']
	set_id_almacen = request.POST['set_id_almacen']
	set_nameProducto = request.POST['set_nameProducto']

	book = xlrd.open_workbook(request.POST['path'] + request.POST['name'])	
	first_sheet = book.sheet_by_index(0)
	#Valida que contenga el sub inventario y el PDV
	if first_sheet.cell(0, 0).value != 'SUBINVENTARIO':
		data = {'error': 'En el archivo falta la celda con la etiqueta SUBINVENTARIO'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	if first_sheet.cell(0, 1).value != 'NOMBRE':
		data = {'error': 'En el archivo falta la celda con la etiqueta NOMBRE'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	if first_sheet.cell(0, 2).value != 'MODELO':
		data = {'error': 'En el archivo falta la celda con la etiqueta MODELO'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	if first_sheet.cell(0, 3).value != 'IMEI':
		data = {'error': 'En el archivo falta la celda con la etiqueta IMEI'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	if first_sheet.cell(0, 4).value != 'FOLIO':
		data = {'error': 'En el archivo falta la celda con la etiqueta FOLIO'}
		return HttpResponse(json.dumps(data), mimetype="application/json")

	for y in range(1, first_sheet.nrows - 1):
		if first_sheet.cell(y, 0).value == set_id_almacen and first_sheet.cell(y, 2).value == set_nameProducto:
			existRecep = recepcion_articulo.objects.filter(imei = str(first_sheet.cell(y, 3).value)).count()
			if existRecep == 0: # El imei no existe entonces next process
				reg = recepcion_articulo(
					ord_det_id 	= set_ord_det_id,
					imei		= str(first_sheet.cell(y, 3).value),
					folio		= str(int(first_sheet.cell(y, 4).value))
				)
				reg.save()
								
				ordenes_det = orden_compra_det.objects.filter(estatus__isnull = True, 
					id = set_ord_det_id)
				# Actualizar existencia en el inventario si no existe crearlo
				existInvt = inventario.objects.filter(id_sub_inventario__sub_inventario = first_sheet.cell(y, 0).value,
					id_articulo__referencia = first_sheet.cell(y, 2).value)
				if existInvt.count() == 0: #add
					reg = inventario(
						id_sub_inventario_id 	= ordenes_det[0].id_sub_inventario_id,
						id_articulo_id			= ordenes_det[0].id_articulo_id,
						existencia				= 1
					)
					reg.save()
				else: #update
					reg2 = inventario.objects.get(id = existInvt[0].id)
					reg2.existencia = reg2.existencia + 1
					reg2.save()

				# Actualizar estatus de la orden de compra a recibido = R
				reg2 = orden_compra_det.objects.get(id = set_ord_det_id)
				reg2.estatus = 'R'
				reg2.save()
				
	context = {}
	return render(request, 'frm_loadFileRM.html', context)