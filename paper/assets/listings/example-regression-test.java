public class ExampleRegressionTest {
  /**
   * Regression: comments cannot be removed if a user changes their first
   * name.
   */
  @Test
  public void testRegression439() {
    Comment comment = CommentSystem.findById(1);
    Assert.assertNotNull(comment);

    // Change the first name.
    Assert.assertEquals("Bert", comment.user.firstName);
    comment.user.setFirstName("Matthew");
    Assert.assertEquals("Matthew", comment.user.firstName);

    // Try to remove the comment.
    comment.remove();
    Assert.assertTrue(comment.removed);
  }
}
