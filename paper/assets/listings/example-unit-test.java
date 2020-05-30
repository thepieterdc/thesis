public class ExampleUnitTest {
  static int square(int base) { return base * base; }

  @Test
  public void testSquare() {
    Assert.assertEquals(25, square(5));
    Assert.assertEquals(4, square(-2));
  }
}
