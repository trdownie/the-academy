/*
Core logic/payment flow for this comes from here:
https://stripe.com/docs/payments/accept-a-payment

CSS from here:
https://stripe.com/docs/stripe-js
*/

/* Get API keys, set base style to match Bootstrap & create card element*/
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');


// Handle realtime validation errors on card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-exclamation-triangle"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

// On submit, apply overlay
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Get whether 'save info' ticked on form
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // Get csrf from form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    // Get required data
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    // Set url to trigger
    var url = '/checkout/cache_checkout_data/';

    // Confirm card payment to Stripe
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    address: {
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.town_or_city.value),
                    },
                    email: $.trim(form.email.value),
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                },
            }
        }).then(function(result) {
            // If there's an error, display the message on screen
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-exclamation-triangle"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            // Otherwise, submit the form
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function(){
        // reload on fail (message will be served from django)
        location.reload();
    })
});