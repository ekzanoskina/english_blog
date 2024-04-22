// Retrieve the CSRF token from the HTML element with ID 'csrf_token'
const csrf_token = document.getElementById("csrf_token").value;

// Function to toggle visibility of a div with ID 'myDIV'
function ShowCommentInput() {
  var x = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

// Function to toggle visibility of a modal dialog for login
function DisplayPopup() {
  var x = document.getElementById("modal_dialog_login");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

// Function to close the modal dialog by setting its display style to 'none'
function CloseModalDialog() {
  const dialog = document.getElementById("modal_dialog_login");
  dialog.style.display = "none";
}

// Function to post a comment.
function postComment() {
  // Retrieve value from the comment input and post ID field
  const comment = document.getElementById('commentInput').value;
  const postId = document.getElementById('postId').value;

  // Post request to submit the comment
  fetch('/submit_comment', {
    method: 'POST',
    headers: {
      "X-CSRFToken": csrf_token, // Use CSRF token for security
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({comment: comment, post_id: postId})
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Update the comment count displayed on the page
      const commentCountElement = document.getElementById('commentCount');
      const currentCount = parseInt(commentCountElement.textContent, 10) || 0;
      const newCount = currentCount + 1;
      commentCountElement.textContent = newCount;

      // If there's no comments section, create one
      if (!document.getElementById('commentsSection')) {
        const commentsSection = document.createElement('div');
        commentsSection.classList.add('card', 'text-dark');
        commentsSection.id = 'commentsSection';
        document.querySelector('.my-2').parentNode.insertBefore(commentsSection, document.querySelector('.my-2').nextSibling);
        const myDiv = document.getElementById('field');
        myDiv.appendChild(commentsSection);
      }

      // Create new div for the new comment
      const newComment = document.createElement('div');

      // Set HTML content for the new comment, including commenter's avatar, name, date posted, and the comment itself.
      newComment.innerHTML = `
        <hr class="my-0" />
        <div class="card-body p-4">
          <div class="d-flex flex-start">
            <img class="rounded-circle shadow-1-strong me-3" id='image'
              src="static/img/${data.image_path}" alt="avatar" width="60"
              height="60" />
            <div>
              <h6 class="fw-bold mb-1">${data.user}</h6>
              <div class="d-flex align-items-center mb-3">
                <p class="mb-0">
                  ${data.date_posted}
                </p>
              </div>
              <p class="mb-0">
                ${data.comment}
              </p>
            </div>
          </div>
      `;

      // Append the new comment to the comments section
      const commentsSection = document.getElementById('commentsSection');
      commentsSection.appendChild(newComment);
      newComment.scrollIntoView({ behavior: "smooth", block: "end" });

      // Clear the comment input field after posting
      document.getElementById("commentInput").value = '';
    }
  });
}