function ShowCommentInput() {
  var x = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
};
function DisplayPopup() {
  var x = document.getElementById("modal_dialog_login");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
};
function postComment() {

  const comment = document.getElementById('commentInput').value;
  const postId = document.getElementById('postId').value;
  fetch('/submit_comment', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({comment: comment, post_id: postId})
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
    // Increment the comment count
        const commentCountElement = document.getElementById('commentCount');
const currentCount = parseInt(commentCountElement.textContent, 10) || 0;
const newCount = currentCount + 1;
commentCountElement.textContent = newCount;

    if (!document.getElementById('commentsSection')) {
  const commentsSection = document.createElement('div');
  commentsSection.classList.add('card', 'text-dark');
  commentsSection.id = 'commentsSection';
  document.querySelector('.my-2').parentNode.insertBefore(commentsSection, document.querySelector('.my-2').nextSibling);
const myDiv = document.getElementById('field');
myDiv.appendChild(commentsSection);
}
const newComment = document.createElement('div');

// Set the innerHTML of the new div element to the desired HTML code
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

// Append the new div element as a child to the parent element
const commentsSection = document.getElementById('commentsSection');
commentsSection.appendChild(newComment);
newComment.scrollIntoView({ behavior: "smooth", block: "end" });
    document.getElementById("commentInput").value = '';
    }
  });

}