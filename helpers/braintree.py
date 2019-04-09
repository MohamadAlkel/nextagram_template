import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="x8s6b3dp65439cgr",
        public_key="tccpr6m8tn3fhbw5",
        private_key="f498b6c9f5685e3c7595a0719f0c606e"
    )
)