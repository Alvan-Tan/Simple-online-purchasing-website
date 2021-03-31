paypal.Buttons({
    style : {
        color: 'blue',
        shape: 'pill'
    },
    createOrder: function (data, actions) {
        return actions.order.create({
            purchase_units : [{
                amount: {
                    value: '399' // have to change and link to price from previous microservices
                }
            }]
        });
    },
    onApprove: function (data, actions) {
        return actions.order.capture().then(function (details) {
            console.log(details)
            console.log(details.status)
            console.log(data)
            // window.location.replace("success.html")
            //invoke shipping microservice
        })
    },
    onCancel: function (data) {
        return console.log(data)
        // window.location.replace("notsuccess.html")
    }
}).render('#paypal-payment-button');