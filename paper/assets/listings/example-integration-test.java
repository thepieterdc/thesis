public class ExampleIntegrationTest {
  @Test
  public void testOrderPizza() {
    // Authenticate a test user.
    Session session = UserSystem.login("JohnDoe", "password");
    session.wallet.balance = 1000.0;
    Assert.assertNotNull(session);

    // Find an item to order.
    Pizza pizza = new Pizza(Flavour.PEPPERONI);
    Assert.assertNotNull(pizza);

    // Create an order.
    Order order = OrderSystem.createOrder(session, pizza);
    Assert.assertNotNull(order);

    // Checkout.
    double oldBalance = session.wallet.balance;
    order.checkout(session.wallet);
    double newBalance = session.wallet.balance;
    Assert.assertEquals(oldBalance - pizza.price, newBalance);
  }
}
