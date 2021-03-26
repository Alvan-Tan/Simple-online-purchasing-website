<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Paypal Payment</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main id="cart-main"> 
        <div class="site-title text-center">
            <h1 class="font-title">Payment Page</h1>
        <div class = "site-title text-center">
                <div id = "paypal-payment-button">
                </div>
        </div>
        <!-- <div class="container">
            <div class="grid">
                <div class="col-1">
                    <div class="flex item justify-content-between">
                        <div class="flex">
                            <div class="img text-center">
                                <img src="./offwhite.jpeg" alt="">
                            </div>
                            <div class="title">
                                <h3>Off- White Nike</h3>
                                <span>Shoes</span>
                                <div class="buttons"> -->
                                    <!-- <button type="submit"><i class="fas fa-chevron-up"></i> </button> -->
                                    <!-- <input type="text" class="font-title" value="1"> -->
                                    <!-- <button type="submit"><i class="fas fa-chevron-down"></i> </button> -->
                                <!-- </div>
                                <a href="#">Save for later</a> |
                                <a href="#">Delete From Cart</a>
                            </div>
                        </div>
                        <div class="price">
                            <h4 class="text-red">$399</h4>
                        </div>
                    </div>
                </div>
                <div class="col-2">
                    <div class="subtotal text-center">
                        <h3>Price Details</h3>
                        <ul>
                            <li class="flex justify-content-between">
                                <label for="price">Products ( 1 item ) : </label>
                                <span>$399</span>
                            </li>
                            <li class="flex justify-content-between"> 
                                <label for="price">Delivery Charges : </label>
                                <span>Free</span>
                            </li>
                            <hr>
                            <li class="flex justify-content-between">
                                <label for="price">Amount Payable : </label>
                                <span class="text-red font-title">$399</span>
                            </li> -->
                            <!-- <li class = "flex justify-content-between">
                                <div id = "paypal-payment-button">
                                </div>
                            </li> -->
                        </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <script src="https://www.paypal.com/sdk/js?client-id=ATtOwXSVt1lZ-0LkVNOGuawBkumaGwh0af_FqpMwuZrY2gIFS4sXLGxVNrH-MqkM7DlV34fZZ7y2l7Pb&disable-funding=credit,card"></script>
    <script src='index.js'></script>
</body>
</html>