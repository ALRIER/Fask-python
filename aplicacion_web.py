#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 19:24:46 2021

@author: alrier
"""

from flask import Flask
from flask import render_template
from flask import Flask,render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
@app.route('/inicio')
def index():
    lg=listaTransito()
    return render_template('inicio.html',transito = lg)

@app.route('/agregar')
def d():
    return render_template ('agregar.html')

@app.route('/mapa')
def e():
    lg=listaTransito()
    return render_template('mapa.html',transito = lg)

#todos los datos que se vayan a crear se deben llamar igual en ambos archvos
#los datos entran en regitrar
@app.route('/registrar', methods=["GET", "POST"])
def registrar():
    Fecha_de_accidente = request.form['Fecha_de_accidente']
    hora_de_accidente = request.form['hora_de_accidente']
    placa = request.form['placa']
    nombre_conductor = request.form['nombre_conductor']
    direccion = request.form['direccion']
    insertatransito(Fecha_de_accidente,hora_de_accidente,placa,nombre_conductor,direccion)
    return redirect(url_for('index'))


#Lista los datos de los gerentes
def listaTransito():
    mongo = MongoClient("localhost",27017)
    dbaccidentes = mongo["accidentes"]
    coleccionTransito =  dbaccidentes["transito"]
    listatransito = coleccionTransito.find()
    mongo.close()
    return ([lg for lg in listatransito]) 


#Registrar nuevo gerente
def insertatransito(Fecha_de_accidente,hora_de_accidente,placa,nombre_conductor,direccion):
    mongo = MongoClient("localhost",27017)
    dbaccidentes = mongo["accidentes"]
    colecciontransito =  dbaccidentes["transito"]
    
    app = Nominatim(user_agent="DEG52")
    direcc = app.geocode(direccion)
    if(direcc != None):
        vdireccion = direcc.address
        latitud = direcc.latitude
        longitud = direcc.longitude
    else:
        vdireccion = direccion
        latitud = ""
        longitud = ""
    
    colecciontransito.insert({"Fecha_de_accidente":Fecha_de_accidente,"hora_de_accidente":hora_de_accidente,"placa":placa, "direccion":vdireccion,"nombre_conductor":nombre_conductor,"latitud":latitud,"longitud":longitud})
    mongo.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
