from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class cat_articulo(models.Model):
	referencia	= models.CharField(max_length = 30, blank = True, null = True)			

class cat_almacen(models.Model):
	sub_inventario 	= models.CharField(max_length = 15, blank = True, null = True)
	pdv				= models.CharField(max_length = 50, blank = True, null = True)
	
class orden_compra_det(models.Model):
	id_sub_inventario = models.ForeignKey(cat_almacen)
	id_articulo 	  = models.ForeignKey(cat_articulo)
	cantidad		  = models.IntegerField()
	estatus			  = models.CharField(max_length = 1, blank = True, null = True)

class recepcion_articulo(models.Model):
	ord_det 			= models.ForeignKey(orden_compra_det)
	imei				= models.CharField(max_length = 50, blank = True, null = True)
	folio				= models.CharField(max_length = 50, blank = True, null = True)

class inventario(models.Model):
	id_sub_inventario = models.ForeignKey(cat_almacen)
	id_articulo 	  = models.ForeignKey(cat_articulo)
	existencia		  = models.IntegerField()


	



	#datos articulos
	# N.ALC5010N
	# N.ALU5DR
	# N.ALU5NG
	# N.HGELIPD
	# N.HGELIPN
	# N.HGWMTDR
	# N.HGWMTGR
	# N.HUM10LN
	# N.HISEF20N
	# N.HISF23D
	# N.HISF23N
	# N.HISF23P
	# N.HISU963D
	# N.HISU963N
	# N.HISU963R
	# N.HP10SBD
	# N.HP10SBN
	# N.HP10SBP
	# N.HP10SBR
	# N.HP10SDR
	# N.HP10SN
	# N.HP10SRS
	# N.HUAP10N
	# N.HUAP9LB
	# N.HUAP9LD
	# N.HUAP9LN
	# N.HUP10LA
	# N.HUP10LD
	# N.HUP10LN
	# N.HUP10PN
	# N.HY517DR
	# N.HY517GR
	# N.HY5LTAZ
	# N.HY5LTDR
	# N.HY5LTGR
	# N.HY5PROD
	# N.HY5PROG
	# N.I7P32B
	# N.I8P256D
	# N.I8P256G
	# N.I8P256P
	# N.IP7128B
	# N.IP7128G
	# N.IP7128J
	# N.IP7128R
	# N.IP7128S
	# N.IP732B
	# N.IP732B
	# MATE
	# N.IP732G
	# N.IP732P
	# N.IP732R
	# N.IP732S
	# N.IP7P128B
	# N.IP7P128G
	# N.IP7P128J
	# N.IP7P128R
	# N.IP7P128S
	# N.IP7P32B
	# N.IP7P32G
	# N.IP7P32R
	# N.IP7P32S
	# N.IP8256D
	# N.IP8256G
	# N.IP8256P
	# N.IP864D
	# N.IP864G
	# N.IP864P
	# N.IP8P256D
	# N.IP8P64D
	# N.IP8P64G
	# N.IP8P64P
	# N.ISE32DR
	# N.ISE32GR
	# N.ISE32PT
	# N.ISE32RS
	# N.J7NEOD
	# N.J7NEON
	# N.J7PROD
	# N.J7PRON
	# N.LX520DR
	# N.LX520NG
	# N.MOG5PD
	# N.MOG5PG
	# N.MOTG5DR
	# N.MOTG5GR
	# N.MOTG5PA
	# N.MOTG5PD
	# N.MOTG5PG
	# N.MOTOCNG
	# N.MOTOEAZ
	# N.MOTOEDR
	# N.MOTOEGR
	# N.MZ2PLYA
	# N.MZ2PLYD
	# N.MZ2PLYG
	# N.SAJ7PRS
	# N.SAMA720D
	# N.SAMA720N
	# N.SAMGPPD
	# N.SAMGPPN
	# N.SAMGPPP
	# N.SAMGPPR
	# N.SAMJ5PN
	# N.SAMJ7PD
	# N.SAMJ7PN
	# N.SAMJ7PR
	# N.SAMS8NG
	# N.SAMS8PT
	# N.SAMS8RS
	# N.SAMS8VT
	# N.SIMATTTRIO2006D
	# N.SIMOPUS1
	# N.SIMOPUSD1
	# N.SIMV8ATTTRIO
	# N.SIMV8ATTTRIOD
	# N.SJ7NEOD
	# N.SJ7NEON
	# N.SJ7PROD
	# N.SJ7PRON
	# N.SJ7PRORS
	# N.SNOTE8N
	# N.SNOTE8V
	# N.SONYL1N
	# N.SONYL1R
	# N.SONYXAUN
	# N.SOXZSNG
	# N.SPLS8NG
	# N.SPLS8PT
	# N.SPLS8VT
	# N.ZTA321A
	# N.ZTA321G
	# N.ZTA521B
	# N.ZTA521N
	# N.ZTE511N
	# N.ZTEA6NG
	# N.ZTEA6PT
	# N.ZV8MNG
	# N.ZV8MPN
