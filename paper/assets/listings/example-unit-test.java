public class ExampleUnitTest {
  static int square(int base) { return base * base; }

  @Test
  void testSquare() {
    Assert.assertEquals(25, square(5));
    Assert.assertEquals(4, square(-2));
    Assert.assertEquals(0, square(0));
  }
}
