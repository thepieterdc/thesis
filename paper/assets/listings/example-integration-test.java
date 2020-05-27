public class ExampleIntegrationTest {
  @Test
  public void testOrderPizza() {
    Session session = UserSystem.login("JohnDoe", "password");
    Assert.assertNotNull(session);

    Pizza order = new Pizza("pepperoni");
    Assert.assertTrue(OrderSystem.order(session, order));
  }
}
