// Function to handle the like button click
function LetLike(event) {
  // Prevent the default form submission behavior

  // Get the post ID from the form data
  const postId = document.getElementById('postId').value;
  var csrf_token = document.getElementById("csrf_token").value
  // Send a POST request to the Flask route to toggle the like
  fetch('/toggle_like', {
    method: 'POST',
    headers: {"X-CSRFToken": csrf_token,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ post_id: postId})
  })
  .then(response => response.json())
  .then(data => {
    // Update the like count on the page
    const likeCountElement = document.getElementById('like-count');
    if (data.liked ) {
    likeCountElement.textContent = data.likes_count - 1;

    }
    else {
    likeCountElement.textContent = data.likes_count + 1;
    }

  });
}
