const searchInput = document.getElementById('search-courses');
const courseGrid = document.getElementById('course-grid');
const resultsCount = document.getElementById('results-count');
const cards = Array.from(courseGrid.querySelectorAll('.course-card'));

// Task 2, step 130: update the aria-live region whenever the visible count changes
function updateResultsCount(count) {
  resultsCount.textContent = `${count} course${count === 1 ? '' : 's'} found`;
}

searchInput.addEventListener('input', (event) => {
  const term = event.target.value.toLowerCase();
  let visibleCount = 0;

  cards.forEach((card) => {
    const name = card.dataset.course.toLowerCase();
    const matches = name.includes(term);
    card.style.display = matches ? '' : 'none';
    if (matches) visibleCount += 1;
  });

  updateResultsCount(visibleCount);
});

// Task 2, step 129: keyboard support - Enter on a focused card behaves like a click
function selectCourse(card) {
  const name = card.dataset.course;
  alert(`Selected course: ${name}`);
}

courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (card) selectCourse(card);
});

courseGrid.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter' && event.key !== ' ') return;
  const card = event.target.closest('.course-card');
  if (card) {
    event.preventDefault();
    selectCourse(card);
  }
});

// Basic profile form handling
const profileForm = document.getElementById('profile-form');
profileForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(profileForm);
  console.log('Profile saved:', Object.fromEntries(formData));
  alert('Profile saved!');
});
