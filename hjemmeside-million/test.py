import os
import pandas as pd

# Brug den absolutte sti til filen, hvis nødvendigt
file_path= 'products - rema.xlsx'

# Læs Excel-filen, ignorer første linje og brug anden linje som kolonnenavne
df = pd.read_excel(file_path, skiprows=1)

# Filtrér uønskede product_types
exclude_types = ["Baby og småbørn", "Personlig pleje", "Husholdning", "Kiosk"]
df = df[~df["/product/product_type"].isin(exclude_types)]

# Få den aktuelle mappe, hvor Python-filen kører
output_dir = os.path.dirname(os.path.abspath(__file__))

# Funktion til at generere HTML for produkter
def generate_product_html(product_group, product_type, show_all=False):
    product_html = ""
    products_to_show = product_group.head(6) if not show_all else product_group
    for index, row in products_to_show.iterrows():
        product_id = f"product{index}"
        # Bruger den fulde URL, som er angivet i Excel-filen
        image_link = row['/product/imageLink']
        if image_link:  # Hvis der er et link til et billede
            image_src = image_link.strip()  # Fuld URL til billedet
        else:
            image_src = "images/default_image.png"  # Fallback billede, hvis ingen billede findes
        
        title = row['/product/title']
        brand = row['/product/brand']
        description = row['/product/description']
        price = row['/product/price']

        # Tilføj HTML for produktet med en grøn boks til at tilføje til kurven
        product_html += f"""
        <div id="{product_id}" class="product" onclick="openOverlay('{product_id}')">
            <img src="{image_src}" alt="{title}">
            <h3>{title}</h3>
            <p class="price">{price}</p>
            <p>{description}</p>
            <p class="brand">{brand}</p>
            <!-- Grøn boks nederst til højre -->
            <div class="corner-box" onclick="addProductToCart('{product_id}')">Tilføj til kurv</div>
        </div>
        """
    return product_html

# Opret HTML-indhold for ugens tilbud
sale_products = df.dropna(subset=['/product/sale_price_effective_date'])
sale_products_html = generate_product_html(sale_products, "Ugens Tilbud")

# Opret HTML for hver product_type
product_types_html = ""
for product_type, group in df.groupby('/product/product_type'):
    product_types_html += f"""
    <div class="product-type">
        <h2>{product_type} <a href="{product_type.replace(' ', '_')}.html">Vis alle</a></h2>
        <div class="products">
            {generate_product_html(group, product_type)}
        </div>
    </div>
    """

# Generer HTML-indhold for forsiden
index_html_content = f"""
<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spotter</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <script src="script.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>Spotter</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Hjem</a></li>
                    <li><a href="sale.html">Ugens Tilbud</a></li>
                </ul>
            </nav>
            <!-- Søgefelt -->
            <div class="search-container">
                <input type="text" id="search-input" placeholder="Søg efter produkter..." oninput="filterProducts()">
            </div>
        </div>
        <!-- Indkøbskurv placeret udenfor containeren -->
        <div class="cart">
            <a href="javascript:void(0);" class="cart-icon" onclick="openCartOverlay()">
                <img src="Kurv.png" alt="Indkøbskurv" class="cart-icon">
                <span id="cart-count">0</span> <!-- Tæller for varer i kurven -->
            </a>
        </div>
    </header>
    <main>
        <div class="container">
            <section class="product-type">
                <h2>Ugens Tilbud <a href="sale.html">Vis alle</a></h2>
                <div class="products" id="sale-products">
                    {sale_products_html}
                </div>
            </section>
            {product_types_html}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2024 Spotter.</p>
        </div>
    </footer>

    <!-- Overlay for produktinformation -->
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <span class="close" onclick="closeOverlay()">&times;</span>
            <img id="overlay-image" src="" alt="Produktbillede">
            <div class="overlay-text">
                <h3 id="overlay-title">Produktnavn</h3>
                <p id="overlay-description">Produktbeskrivelse</p>
                <p id="overlay-brand">Mærke: <span id="overlay-brand-name"></span></p>
                <p id="overlay-price">Pris: <span id="overlay-price-value"></span></p>
            </div>
        </div>
    </div>

    <!-- Overlay for indkøbskurv -->
    <div id="cart-overlay" class="overlay">
        <div class="overlay-content">
            <span class="close" onclick="closeCartOverlay()">&times;</span>
            <h2>Indkøbskurv</h2>
            <div id="cart-items">
                <!-- Dynamiske produkter i kurven -->
                <div class="cart-item">
                    <img src="images/default_image.png" alt="Produktbillede" class="cart-item-img">
                    <div class="cart-item-info">
                        <h3 class="cart-item-title">Produktnavn</h3>
                        <p class="cart-item-price">Pris: 99,99 kr</p>
                    </div>
                </div>
            </div>
            <button id="checkout-button">Gå til kassen</button>
        </div>
    </div>
</body>
</html>
"""

# Skriv index.html filen
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
    file.write(index_html_content)

# Generer HTML for hver product_type (vis alle sider)
for product_type, group in df.groupby('/product/product_type'):
    product_html_content = f"""
    <!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_type}</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <script src="script.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>{product_type}</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Hjem</a></li>
                    <li><a href="sale.html">Ugens Tilbud</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <main>
        <div class="container">
            <div class="products">
                {generate_product_html(group, product_type, show_all=True)}
            </div>
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2024 Spotter.</p>
        </div>
    </footer>
</body>
</html>
    """
    file_name = product_type.replace(' ', '_') + ".html"
    with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as file:
        file.write(product_html_content)

# Generer HTML for alle sale products (ugens tilbud siden)
sale_html_content = f"""
<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ugens Tilbud</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <script src="script.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>Ugens Tilbud</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Hjem</a></li>
                    <li><a href="sale.html">Ugens Tilbud</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <main>
        <div class="container">
            <div class="products">
                {generate_product_html(sale_products, "Ugens Tilbud", show_all=True)}
            </div>
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2024 Spotter.</p>
        </div>
    </footer>
</body>
</html>
"""

# Skriv sale.html filen
with open(os.path.join(output_dir, "sale.html"), "w", encoding="utf-8") as file:
    file.write(sale_html_content)
