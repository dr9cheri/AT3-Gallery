// script.js
document.addEventListener('DOMContentLoaded', () => {
    const cutoutText = document.getElementById('cutoutText');
    const imageGallery = document.getElementById('imageGallery');
    const searchBar = document.getElementById('searchBar');
    const hashtagMenu = document.getElementById('hashtagMenu');
    
    // const images = [
    //     { URL: '../static/images/babypanda.jpg', hashtag: ['#panda', 'animal'] },
    //     { URL: '../static/images/panda.jpg', hashtag: ['#panda', '#animal'] },
    //     { URL: '../static/images/pandaintree.jpg', hashtag: ['#panda', '#animal'] },
    //     { URL: '../static/images/sleeppanda.jpg', hashtag: ['#panda', '#animal'] },
    //     // Add more images and hashtag here
    // ];

    const hashtag = new Set();

    // Populate the image gallery and hashtag
    image_list.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = image.URL;
        imgElement.alt = image.hashtag.join(' ');
        imageGallery.appendChild(imgElement);

        image.hashtag.forEach(tag => hashtag.add(tag));
    });
    // console.log(hashtag);
    // Populate the hashtag menu
    hashtag.forEach(tag => {
        const liElement = document.createElement('li');
        const aElement = document.createElement('li');
        aElement.href = "#";
        aElement.textContent = tag;
        aElement.addEventListener('click', () => filterImagesByHashtag(tag));
        liElement.appendChild(aElement);
        hashtagMenu.appendChild(liElement);
    });

    // Click event for cutout text to reveal the image gallery
    cutoutText.addEventListener('click', () => {
        imageGallery.style.display = imageGallery.style.display === 'flex' ? 'none' : 'flex';
    });

    // Search bar functionality
    searchBar.addEventListener('input', () => {
        const query = searchBar.value.toLowerCase();
        filterImagesByQuary(query);
    });

    function filterImagesByHashtag(tag) {
        const image = imageGallery.querySelectorAll('img');
        image.forEach(img => {
            img.style.display = img.alt.includes(tag) ? 'block' : 'none';
        });
    }
});