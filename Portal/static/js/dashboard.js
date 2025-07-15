// CSRF & URLs are assumed to be passed in template
// <script> const csrfToken = "{{ csrf_token }}"; const addUrl = "{% url 'add_student' %}"; </script>

document.addEventListener("DOMContentLoaded", () => {
  // Add Student Form Submit
  const addForm = document.getElementById("addStudentForm");
  if (addForm) {
    addForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const errorDiv = document.getElementById("formError");
      errorDiv.classList.add("hidden");
      errorDiv.textContent = "";
      if (!validateStudentForm(this)) return;

      const formData = new FormData(this);
      fetch(addUrl, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
      })
        .then((response) =>
          response
            .json()
            .then((data) => ({ status: response.status, body: data }))
        )
        .then(({ status, body }) => {
          if (status === 200 && body.status === "success") {
            addForm.reset();
            document.getElementById("addModal").classList.add("hidden");
            window.location.reload();
          } else {
            errorDiv.textContent = body.error || "An error occurred.";
            errorDiv.classList.remove("hidden");
          }
        })
        .catch(() => {
          errorDiv.textContent = "Something went wrong. Try again later.";
          errorDiv.classList.remove("hidden");
        });
    });
  }
});

// Delete Student
function deleteStudent(id) {
  if (confirm("Are you sure you want to delete this student?")) {
    fetch(`/delete-student/${id}/`, {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
    }).then(() => window.location.reload());
  }
}

// Validate Add/Edit Form
function validateStudentForm(form) {
  const name = form.querySelector('[name="name"]').value.trim();
  const subject = form.querySelector('[name="subject"]').value.trim();
  const marks = form.querySelector('[name="marks"]').value.trim();

  const nameRegex = /^[A-Za-z ]{2,}$/;
  const subjectRegex = /^[A-Za-z ]{2,}$/;

  form.querySelectorAll(".form-error")?.forEach((el) => el.remove());

  let valid = true;

  function showError(input, message) {
    const error = document.createElement("div");
    error.classList.add("form-error");
    error.innerText = message;
    input.after(error);
    valid = false;
  }

  const nameInput = form.querySelector('[name="name"]');
  const subjectInput = form.querySelector('[name="subject"]');
  const marksInput = form.querySelector('[name="marks"]');

  if (!nameRegex.test(name))
    showError(nameInput, "Name must be at least 2 letters.");
  if (!subjectRegex.test(subject))
    showError(subjectInput, "Subject must be at least 2 letters.");
  const marksValue = Number(marks);
  if (isNaN(marksValue) || marksValue < 0 || marksValue > 100)
    showError(marksInput, "Marks must be between 0 and 100.");

  return valid;
}

// Inline Editing Start
function startInlineEdit(link) {
  const row = link.closest("tr");
  row
    .querySelectorAll(".student-name, .student-subject, .student-marks")
    .forEach((el) => el.classList.add("d-none"));
  row
    .querySelectorAll(".edit-name, .edit-subject, .edit-marks")
    .forEach((el) => el.classList.remove("d-none"));
  row.querySelector(".action-dropdown").classList.add("d-none");
  row.querySelector(".edit-actions").classList.remove("d-none");
}

// Inline Cancel
function cancelInlineEdit(btn) {
  const row = btn.closest("tr");
  row
    .querySelectorAll(".student-name, .student-subject, .student-marks")
    .forEach((el) => el.classList.remove("d-none"));
  row
    .querySelectorAll(".edit-name, .edit-subject, .edit-marks")
    .forEach((el) => el.classList.add("d-none"));
  row.querySelector(".action-dropdown").classList.remove("d-none");
  row.querySelector(".edit-actions").classList.add("d-none");
  row
    .querySelectorAll(".form-error-inline, .inline-edit-error")
    .forEach((el) => el.remove());
}

// Inline Save
function saveInlineEdit(btn, id) {
  const row = btn.closest("tr");
  const nameInput = row.querySelector(".edit-name");
  const subjectInput = row.querySelector(".edit-subject");
  const marksInput = row.querySelector(".edit-marks");

  const name = nameInput.value.trim();
  const subject = subjectInput.value.trim();
  const marks = marksInput.value.trim();

  let errorEl = row.querySelector(".inline-edit-error");
  if (!errorEl) {
    errorEl = document.createElement("div");
    errorEl.classList.add(
      "inline-edit-error",
      "text-danger",
      "text-sm",
      "mt-2"
    );
    row.lastElementChild.appendChild(errorEl);
  }
  errorEl.classList.add("d-none");
  errorEl.textContent = "";

  // Validation
  const nameRegex = /^[A-Za-z ]{2,}$/;
  const subjectRegex = /^[A-Za-z ]{2,}$/;
  const marksValue = Number(marks);

  if (!nameRegex.test(name)) {
    errorEl.textContent =
      "Name must be at least 2 characters (letters and spaces only)";
    errorEl.classList.remove("d-none");
    return;
  }

  if (!subjectRegex.test(subject)) {
    errorEl.textContent =
      "Subject must be at least 2 characters (letters and spaces only)";
    errorEl.classList.remove("d-none");
    return;
  }

  if (isNaN(marksValue) || marksValue < 0 || marksValue > 100) {
    errorEl.textContent = "Marks must be between 0 and 100.";
    errorEl.classList.remove("d-none");
    return;
  }

  // Update request
  const formData = new FormData();
  formData.append("name", name);
  formData.append("subject", subject);
  formData.append("marks", marks);
  formData.append("csrfmiddlewaretoken", csrfToken);

  fetch(`/update-student/${id}/`, {
    method: "POST",
    body: formData,
  })
    .then((response) =>
      response.json().then((data) => ({ status: response.status, body: data }))
    )
    .then(({ status, body }) => {
      if (status === 200 && body.status === "updated") {
        window.location.reload();
      } else {
        const errorMsg =
          typeof body.error === "string"
            ? body.error
            : "Update failed. Please check your inputs.";
        errorEl.textContent = errorMsg;
        errorEl.classList.remove("d-none");
      }
    })
    .catch(() => {
      errorEl.textContent = "Something went wrong. Try again later.";
      errorEl.classList.remove("d-none");
    });
}
