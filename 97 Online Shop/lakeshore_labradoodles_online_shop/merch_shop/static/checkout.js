// This is your test publishable API key.
const stripe = Stripe("pk_test_51PCjpr2NyZPCpoqgxgGN7kwRQhlkuNQ9iKqCiotBa8hi0PoKwLbGePm19ScHnGzloWNILhWsZUsd3WxEScLP2tO200VjQK2I4g");

initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    const response = await fetch("/create-checkout-session", {
      method: "POST",
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}