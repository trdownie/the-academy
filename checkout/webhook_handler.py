from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order
from articles.models import Article
from academics.models import Academic

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send confirmation email upon order confirmed
        """

        # Get the customer's email address
        customer_email = order.email

        # Compose the email from the templates
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        # Send the email
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def update_proposals(self, order):
        """
        Update any stakes paid (the purchase of a proposal, not an order)
        """

        # Check if an article is a proposal - if so update
        for article in order.order_items.all():
            if article.proposal:
                article = article  # newly defined article for each iteration
                article.stakers += 1
                article.save()

    def handle_event(self, event):
        print("unknown event")
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        # Obtain relevant details, including from intent
        print("intent succeeded")
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        order_total = round(intent.charges.data[0].amount / 100, 2)
        print("intent succeeded 2")
        # Update profile info if save_info box checked 
        # (and user logged in - not AnonymousUser)
        academic = None
        print("intent succeeded 3")
        username = intent.metadata.username
        if username != 'AnonymousUser':
            print('user authenticated')
            academic = Academic.objects.get(user__username=username)
            if save_info:
                print('save info checked')
                academic.default_phone_number = billing_details.phone
                academic.default_country = billing_details.address.country
                academic.default_postcode = billing_details.address.postal_code
                academic.default_town_or_city = billing_details.address.city
                academic.default_street_address1 = billing_details.address.line1
                academic.default_street_address2 = billing_details.address.line2
                academic.default_county = billing_details.address.state
                academic.save()
        print("intent succeeded 4")
        # Loop to try 5 times to find order (1s apart)
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
                print('order found! (try loop)')
                order_exists = True
                break
            except Order.DoesNotExist:
                print('order does not exist! (try loop)')
                attempt += 1
                time.sleep(1)
        print("intent succeeded 5")
        # If order was found in above loop, send message/trigger methods
        if order_exists:
            print('Success 1')
            self.update_proposals(order)
            self._send_confirmation_email(order)
            return HttpResponse(content=f'Webhook received: {event["type"]} \
                                | SUCCESS: Order exists in database',
                                status=200)
        # Otherwise create the order from the bag (from the intent)
        else:
            print('Creating the order')
            order = None
            try:
                order = Order.objects.create(
                    full_name=billing_details.name,
                    academic=academic,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                print('Order created (try loop 2)')
                for article_id, article_count in json.loads(bag).items():
                    article = get_object_or_404(Article, pk=article_id)
                    order.order_items.add(article)
                print('Saving created order')
                order.save()
            # If order cannot be successfully created, 
            # delete order item & return error
            except Exception as e:
                print('PROBLEM!!!!!!')
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        print("intent succeeded 6")
        # If order was successfully created (by Stripe),
        # send confirmation emails/trigger methods 
        self._send_confirmation_email(order)
        self.update_proposals(order)
        print('Success 2')
        return HttpResponse(content=f'Webhook received: {event["type"]} \
                            | SUCCESS: Created order in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print("intent failed")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
