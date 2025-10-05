document.addEventListener('DOMContentLoaded', () => {

    const cart = [];
    const addButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartItemsContainer = document.querySelector('.cart-items');
    const cartTotalElement = document.querySelector('.cart-total');
    const checkoutButton = document.querySelector('.checkout-btn');

    function updateCartDisplay() {
        cartItemsContainer.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<li style="text-align: center; color: var(--secondary-text);">Your cart is empty</li>';
            cartTotalElement.textContent = 'Total: ₹0';
            return;
        }
        
        cart.forEach(item => {
            const li = document.createElement('li');
            li.classList.add('cart-item');
            li.innerHTML = `
                <span>${item.name} (x${item.quantity})</span>
                <span>₹${item.price * item.quantity}</span>
            `;
            cartItemsContainer.appendChild(li);
            total += item.price * item.quantity;
        });

        cartTotalElement.textContent = `Total: ₹${total}`;
    }

    addButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const menuItem = event.target.closest('.menu-item');
            const itemName = menuItem.querySelector('h3').textContent;
            const itemPriceText = menuItem.querySelector('.item-price').textContent;
            const itemPrice = parseFloat(itemPriceText.replace('₹', ''));
            const existingItem = cart.find(item => item.name === itemName);

            if (existingItem) {
                existingItem.quantity++;
            } else {
                cart.push({ name: itemName, price: itemPrice, quantity: 1 });
            }
            
            updateCartDisplay();
        });
    });
    
    if (checkoutButton) {
        checkoutButton.addEventListener('click', (event) => {
            event.preventDefault();

            // NEW: Check if the cart is empty
            if (cart.length === 0) {
                alert("Your cart is empty. Please add items before checking out.");
                return; // Stop the function here
            }
            
            localStorage.setItem('cart', JSON.stringify(cart));
            window.location.href = '/checkout';
        });
    }

    updateCartDisplay();
});