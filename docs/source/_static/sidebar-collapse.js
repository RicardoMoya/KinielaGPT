/**
 * Script para hacer las secciones del sidebar colapsables
 * Estilo GitBook
 */

document.addEventListener('DOMContentLoaded', function() {
    // Encontrar todos los captions en el sidebar
    const captions = document.querySelectorAll('.sidebar-tree .caption');
    
    captions.forEach(function(caption) {
        // Agregar evento de click
        caption.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle de la clase collapsed
            this.classList.toggle('collapsed');
            
            // Guardar el estado en localStorage
            const captionText = this.textContent.trim();
            const isCollapsed = this.classList.contains('collapsed');
            localStorage.setItem('sidebar-' + captionText, isCollapsed ? 'collapsed' : 'expanded');
        });
        
        // Restaurar el estado desde localStorage
        const captionText = caption.textContent.trim();
        const savedState = localStorage.getItem('sidebar-' + captionText);
        
        if (savedState === 'collapsed') {
            caption.classList.add('collapsed');
        }
    });
    
    // Expandir automáticamente la sección que contiene la página actual
    const currentLink = document.querySelector('.sidebar-tree .current');
    if (currentLink) {
        // Buscar el caption padre más cercano
        let parent = currentLink.closest('ul');
        while (parent) {
            const caption = parent.previousElementSibling;
            if (caption && caption.classList.contains('caption')) {
                caption.classList.remove('collapsed');
            }
            parent = parent.parentElement ? parent.parentElement.closest('ul') : null;
        }
    }
});
