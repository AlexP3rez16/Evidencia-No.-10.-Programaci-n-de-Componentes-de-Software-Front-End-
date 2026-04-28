// main.js – Biblioteca Ducky

function confirmDelete(isbn, titulo) {
  const modal = document.getElementById('deleteModal');
  if (!modal) return;
  document.getElementById('deleteModalText').textContent =
    '¿Estas seguro(a) que quieres eliminar el libro ' + titulo + '?';
  document.getElementById('deleteForm').action = '/libros/' + encodeURIComponent(isbn) + '/eliminar';
  modal.style.display = 'flex';
}

function closeDeleteModal() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.style.display = 'none';
}

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeDeleteModal();
});
