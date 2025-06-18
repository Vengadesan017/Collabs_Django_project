const container = document.querySelector('.scroll-container');
const dots = document.querySelectorAll('.dot');

function updateActiveDot() {
  const scrollLeft = container.scrollLeft;
  const containerWidth = container.offsetWidth;
  const index = Math.round(scrollLeft / containerWidth);

  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
  });
}

container.addEventListener('scroll', () => {
  // Throttle the update for better performance
  clearTimeout(container.scrollTimeout);
  container.scrollTimeout = setTimeout(updateActiveDot, 100);
});

// Initialize first dot
updateActiveDot();
