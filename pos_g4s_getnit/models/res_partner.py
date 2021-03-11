import requests
import html.parser
import html
import xml.etree.ElementTree as ET
from odoo import models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def get_nit_name_from_vat(self, vat):
        if vat:
            nit = vat.replace("-", "")
            body = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns0="http://tempuri.org/"><SOAP-ENV:Header/><SOAP-ENV:Body><ns0:getNIT><ns0:vNIT>{}</ns0:vNIT><ns0:Entity>{}</ns0:Entity><ns0:Requestor>{}</ns0:Requestor></ns0:getNIT></SOAP-ENV:Body></SOAP-ENV:Envelope>'.format(nit,self.env.company.vat, self.env.company.requestor_fel)
            #body = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns0="http://tempuri.org/"><SOAP-ENV:Header/><SOAP-ENV:Body><ns0:getNIT><ns0:vNIT>{}</ns0:vNIT><ns0:Entity>86362569</ns0:Entity><ns0:Requestor>9C73426B-EFEF-4C03-9AC4-F0D5761560FF</ns0:Requestor></ns0:getNIT></SOAP-ENV:Body></SOAP-ENV:Envelope>'.format(nit)
            headers = {"Content-Type": "text/xml"}
            r = requests.post(
                'https://fel.g4sdocumenta.com/ConsultaNIT/ConsultaNIT.asmx', data=body, headers=headers)
            xmlroot = ET.fromstring(r.text)
            if xmlroot.findall(".//{http://tempuri.org/}Result")[0].text == 'true':
                nombre = xmlroot.findall(
                    ".//{http://tempuri.org/}nombre")[0].text
                nombre_facturacion_fel = html.parser.HTMLParser().unescape(nombre)
                return {'name': nombre_facturacion_fel}
            else:
                return {'error': 'Datos no encontrados. Verifique si el NIT es correcto.'}
        return {'error': 'Datos no encontrados. Verifique si el NIT es correcto.'}
