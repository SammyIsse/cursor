// Global variabel til at holde styr på indkøbskurven
var cart = [];

// Funktion til at opdatere indkøbskurven (viser antal varer i kurven)
function updateCart() {
    var cartCount = document.getElementById('cart-count');
    cartCount.innerText = cart.length; // Opdaterer antallet af varer i indkøbskurven

    // Hvis der er varer i kurven, vis tælleren, ellers skjul den
    if (cart.length > 0) {
        cartCount.style.display = 'inline'; // Vis tælleren, når der er varer i kurven
    } else {
        cartCount.style.display = 'none'; // Skjul tælleren, hvis kurven er tom
    }
}

// Funktion til at tilføje en vare til indkøbskurven
function addToCart(productId) {
    var productElement = document.getElementById(productId);
    if (!productElement) {
        console.error('Produktet blev ikke fundet:', productId);
        return;
    }

    // Hent produktdata
    var title = productElement.querySelector('h3').innerText;
    var price = productElement.querySelector('.price').innerText.replace(' DKK', '');
    var imageSrc = productElement.querySelector('img').src;

    // Opret et produktobjekt
    var product = {
        id: productId,
        title: title,
        price: price,
        imageSrc: imageSrc
    };

    // Tilføj produktet til indkøbskurven
    cart.push(product);

    // Opdater kurven
    updateCart();

    // Spil animationen for produktet
    playAddToCartAnimation(productElement);
}

// Funktion til at spille animation, når et produkt tilføjes til kurven
function playAddToCartAnimation(productElement) {
    // Tilføj animationen
    productElement.classList.add('added-to-cart'); // Tilføj klasse til produktet

    // Fjern animationen efter 0.5 sek (så den kan afspilles igen næste gang)
    setTimeout(function() {
        productElement.classList.remove('added-to-cart');
    }, 500); // Sørg for at tiden er lang nok til at animationen kan afspilles
}

// Funktion til at åbne indkøbskurv-overlayet
function openCartOverlay() {
    var cartOverlay = document.getElementById('cart-overlay');
    cartOverlay.classList.add('open'); // Tilføj 'open' klasse for at vise overlayet
    displayCartItems(); // Vis indholdet af kurven
}

// Funktion til at lukke indkøbskurv-overlayet
function closeCartOverlay() {
    var cartOverlay = document.getElementById('cart-overlay');
    cartOverlay.classList.remove('open'); // Fjern 'open' klasse for at skjule overlayet
}

// Funktion til at vise indholdet af indkøbskurven
function displayCartItems() {
    var cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = ''; // Ryd tidligere indhold

    // Gennemgå hvert produkt i indkøbskurven og tilføj til visningen
    cart.forEach(function(item) {
        var cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');

        // HTML-indhold for at vise billede, navn og pris
        var itemContent = `
            <div class="cart-item-content">
                <img src="${item.imageSrc}" alt="${item.title}" class="cart-item-image" />
                <div class="cart-item-info">
                    <h4>${item.title}</h4>
                    <p>${item.price} DKK</p>
                </div>
            </div>
            <button class="remove-item" onclick="removeFromCart('${item.id}')">Fjern</button>
        `;

        cartItem.innerHTML = itemContent;
        cartItemsContainer.appendChild(cartItem);
    });
}

// Funktion til at fjerne produkt fra indkøbskurv
function removeFromCart(productId) {
    cart = cart.filter(function(item) {
        return item.id !== productId;
    });
    displayCartItems(); // Opdater indkøbskurv visningen
    updateCart(); // Opdater kurv tælleren
}

// Funktion til at åbne produktinformation overlayet
function openOverlay(productId) {
    var productElement = document.getElementById(productId);

    if (!productElement) {
        console.error('Produktet blev ikke fundet:', productId);
        return;
    }

    // Hent produktdata
    var imageSrc = productElement.querySelector('img').src;
    var title = productElement.querySelector('h3').innerText;
    var description = productElement.querySelector('p:nth-of-type(2)').innerText;
    var brand = productElement.querySelector('.brand').innerText;
    var price = productElement.querySelector('.price').innerText.replace(' DKK', '');

    // Indsæt data i overlayet
    document.getElementById('overlay-image').src = imageSrc;
    document.getElementById('overlay-title').innerText = title;
    document.getElementById('overlay-description').innerText = description;
    document.getElementById('overlay-brand-name').innerText = brand.replace('Mærke: ', '');
    document.getElementById('overlay-price-value').innerText = price + ' DKK';

    // Vis overlayet
    document.getElementById('overlay').style.display = 'block';
    document.body.classList.add('no-scroll'); // Forhindre scrolling bag overlayet
}

// Funktion til at lukke produktinformation overlayet
function closeOverlay() {
    document.getElementById('overlay').style.display = 'none';
    document.body.classList.remove('no-scroll');
}

// Luk overlay ved klik udenfor indholdet
window.onclick = function(event) {
    var overlay = document.getElementById('overlay');
    if (event.target === overlay) {
        closeOverlay();
    }

    var cartOverlay = document.getElementById('cart-overlay');
    if (event.target === cartOverlay) {
        closeCartOverlay();
    }
}

// Når dokumentet er klar, tilføj event listeners til de grønne bokse i produktboksene
document.addEventListener('DOMContentLoaded', function() {
    var productElements = document.querySelectorAll('.product');

    // Gennemgå alle produkter og tilføj event listeners til de grønne bokse
    productElements.forEach(function(productElement) {
        var greenBox = productElement.querySelector('.corner-box'); // Find den grønne boks
        if (greenBox) {
            greenBox.addEventListener('click', function(event) {
                event.stopPropagation(); // Stop klik hændelsen fra at trigge produkt klik
                var productId = productElement.id; // Brug produktets ID som reference
                addToCart(productId); // Tilføj produktet til indkøbskurven
            });
        }

        // Event listener for klik på produktet (åbner produktinfo)
        productElement.addEventListener('click', function() {
            var productId = this.id;
            openOverlay(productId);
        });
    });

    // Åbn indkøbskurv-overlayet ved klik på indkøbskurv-ikonet
    var cartIcon = document.getElementById('cart-icon');
    cartIcon.addEventListener('click', openCartOverlay);
    
    // Luk indkøbskurv-overlayet ved klik på krydset
    var closeCart = document.getElementById('close-cart');
    closeCart.addEventListener('click', closeCartOverlay);

    // Skjul tælleren ved indlæsning af siden, hvis kurven er tom
    updateCart();  // Opdaterer tælleren korrekt ved indlæsning af siden
});

// Funktion til at filtrere produkter baseret på søgeinput
function filterProducts() {
    var searchQuery = document.getElementById('search-input').value.toLowerCase(); // Hent søgetekst
    var productElements = document.querySelectorAll('.product'); // Find alle produkter

    // Gå igennem alle produkter og skjul de der ikke matcher søgeordet
    productElements.forEach(function(productElement) {
        var productName = productElement.querySelector('h3').innerText.toLowerCase(); // Produktnavn
        if (productName.includes(searchQuery)) {
            productElement.style.display = 'block'; // Vis produktet hvis det matcher
        } else {
            productElement.style.display = 'none'; // Skjul produktet hvis det ikke matcher
        }
    });
}

// Event listener for søgefeltet
document.getElementById('search-input').addEventListener('input', filterProducts);

// Funktion til at rydde søgefeltet og vise alle produkter
function clearSearch() {
    document.getElementById('search-input').value = ''; // Ryd søgefeltet
    var productElements = document.querySelectorAll('.product'); // Find alle produkter

    // Vis alle produkter
    productElements.forEach(function(productElement) {
        productElement.style.display = 'block';
    });
}
