public class ExampleRegressionTest {
  // Regression #439: A user cannot remove their comments after they have changed their first name.
  @Test
  public void testRegression439() {
    // Authenticate a test user.
    Session session = UserSystem.login("johndoe", "password");
    Assert.assertNotNull(session);
    
    // Create a comment.
    String content = "This is a comment by John Doe.";
    Comment comment = CommentSystem.create(content, session);
    Assert.assertNotNull(comment);
    
    // Change the first name of the user.
    Assert.assertEquals("Bert", session.user.firstName);
    session.user.setFirstName("Matthew");
    Assert.assertEquals("Matthew", session.user.firstName);
    Assert.assertEquals("Matthew", comment.user.firstName);
    
    // Try to remove the comment.
    CommentSystem.remove(comment);
    Assert.assertTrue(comment.removed);
  }
}
