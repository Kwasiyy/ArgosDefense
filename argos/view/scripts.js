function showImages(diagramType) {
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = ''; // Clear the current images

    // Example images, replace with actual image sources
    const images = {
        'sequence-diagrams': ['sequence-diagram1.png'],
        'high-level-diagrams': ['high-level-diagram1.png'],
        'class-diagrams': ['class-diagram1.png'],
        'use-case-diagrams': ['use-case-diagram1.png'],
    };

    images[diagramType].forEach(src => {
        const img = document.createElement('img');
        img.src = src;
        img.alt = `${diagramType} diagram`;
        imageContainer.appendChild(img);
    });
}