# Using the Braintree API in Objective C & Django to process a subscription payment

This is an example of the Braintree API using the official Objective C & Python SDK's to set up a subscription.

This demo performs the following technical implementations:

* Pulling existing plans from Braintree server
* Creating a new customer
* Processing a subscription

## Technology

This demo uses

* Xcode 6.1+
* [AFNetworking](http://github.com/AFNetworking/AFNetworking)
* [Braintree Client SDK for iOS](http://github.com/braintree/braintree_ios)
* [Braintree Python SDK](https://github.com/braintree/braintree_python)
* [Cocoapods](http://cocoapods.org/): the dependency manager for Objective-C projects.

The sample backend is written in Python and uses:

* [Python](https://www.python.org/): V.2.7.6.
* [Django](https://www.djangoproject.com/): Python web framework. V. 1.7.1.
* The [Braintree Python SDK](https://github.com/braintree/braintree_python)

## Running the server

* In the `server` folder
	* Run `pip install braintree` to install Braintree
	* Run `python manage.py runserver` to start the server

## Running the mobile app (Device / Emulator)

* In the `client` folder
	* Run `pod install` to install all dependencies.
	* Open the newly created file `vzero.xcworkspace` in your XCode.
	* Build the app and run it in your emulator or on your device
		* *Once the app started it will try to get the client token from your backend. Ensure that your server is already running before you launch the mobile application.*
	* Click on `Start Payment`
	* Select either of these payment methods:
		* (PayPal)
			* Fill in the following credentials:
				* Email: `us-customer@commercefactory.org`
				* Password: `test1234`
			* Click `Agree` to accept future payments
		* (Credit Card) Fill in the following credentials:
			* Number: `4111 1111 1111 1111`
			* Expiration date: `11/15`
  			* CVV: `123`
	* Click on `Pay`
	* You will see a message that says __"Subscription ID: [subscription_id]"__


## Useful links

* [Full documentation for the Braintree Client SDK for iOS+Python](https://developers.braintreepayments.com/ios+python/start/overview)
