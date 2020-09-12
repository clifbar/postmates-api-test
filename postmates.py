from flask import Flask, redirect, url_for, render_template, session

import filters, constants

import iso8601
import pytz
import requests
import json
import os

import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return redirect(url_for('order'))

@app.route('/order/')
def order():
    with open('order.json') as f:
        order = json.load(f)
        session['order'] = order
    
    payload = {
      'pickup_address': order['pickup']['address'], 
      'dropoff_address': order['dropoff']['address']
    }

    quote_response = requests.post(constants.QUOTE_ENDPOINT, data=payload, auth=(constants.API_KEY, ''))
    quote = quote_response.json()    
    session['quote_id'] = quote['id']

    return render_template('order.html', order=order, quote=quote)

@app.route('/delivery/')
def delivery():
    if 'quote_id' and 'order' in session:
        order = session['order']
        payload = {
          'dropoff_address': order['dropoff']['address'], 
          'dropoff_name': order['dropoff']['name'], 
          'dropoff_phone_number': order['dropoff']['phone_number'], 
          'manifest':'fancy hot selling socks', 
          'pickup_name': order['pickup']['name'],
          'pickup_address': order['pickup']['address'],
          'pickup_phone_number': order['pickup']['phone_number']
        }
        delivery_response = requests.post(constants.DELIVERY_ENDPOINT, data=payload, auth=(constants.API_KEY, ''))

        return render_template('delivery.html', delivery=delivery_response.json())    
    else:
        return redirect(url_for('order'))


@app.template_filter('currency')
def currency(value):
    value = float(value)/100
    return "${:,.2f}".format(value)

@app.template_filter('format_datetime')
def format_datetime(value):
    tz = pytz.timezone('US/Pacific')
    return iso8601.parse_date(value).astimezone(tz).strftime('%m/%d/%y @ %I:%M %p')


@app.context_processor
def utility_processor():
    def time_from_now(value):
        now = datetime.datetime.now()
        tz = pytz.timezone('US/Pacific')
        timedelta = iso8601.parse_date(value).astimezone(tz).replace(tzinfo=None) - now
        return  '%s minutes from now' % int(timedelta.total_seconds() / 60)
    return dict(time_from_now=time_from_now)
