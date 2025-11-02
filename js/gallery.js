document.addEventListener('DOMContentLoaded', function() {
    const galleryGrid = document.querySelector('.gallery-grid');
    
    // Exemple de données pour la galerie
    const galleryItems = [
        { image: 'images/image1.jpg', title: 'Image 1' },
        { image: 'images/image2.jpg', title: 'Image 2' },
        { image: 'images/image3.jpg', title: 'Image 3' },
        // Ajoutez plus d'images selon vos besoins
    ];

    // Création des éléments de la galerie
    galleryItems.forEach(item => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        
        const img = document.createElement('img');
        img.src = item.image;
        img.alt = item.title;
        
        galleryItem.appendChild(img);
        galleryGrid.appendChild(galleryItem);
    });
}); 