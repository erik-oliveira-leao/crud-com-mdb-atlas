const API_URL = '/produtos';

// DOM Elements
const productsGrid = document.getElementById('products-grid');
const addProductBtn = document.getElementById('add-product-btn');
const modal = document.getElementById('product-modal');
const closeModalBtn = document.getElementById('close-modal');
const productForm = document.getElementById('product-form');
const modalTitle = document.getElementById('modal-title');
const toast = document.getElementById('toast');

// Form Inputs
const inputId = document.getElementById('product-id');
const inputNome = document.getElementById('nome');
const inputPreco = document.getElementById('preco');
const inputDescricao = document.getElementById('descricao');
const inputImagem = document.getElementById('imagem');

// Fetch and display products
async function fetchProducts() {
    try {
        const response = await fetch(API_URL);
        const products = await response.json();
        
        productsGrid.innerHTML = '';
        
        if (products.length === 0) {
            productsGrid.innerHTML = `
                <div class="empty-state">
                    <h3>Nenhum produto encontrado</h3>
                    <p>Adicione um novo produto para começar.</p>
                </div>
            `;
            return;
        }

        products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            
            // Generate a placeholder image based on name if no image is provided
            const imageUrl = product.imagem || `https://ui-avatars.com/api/?name=${encodeURIComponent(product.nome)}&background=3b82f6&color=fff&size=200&font-size=0.33`;
            const price = parseFloat(product.preco).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
            
            card.innerHTML = `
                <img src="${imageUrl}" alt="${product.nome}" class="product-image" onerror="this.src='https://via.placeholder.com/200x200/1e293b/f8fafc?text=Sem+Imagem'">
                <div class="product-info">
                    <h3 class="product-name">${product.nome}</h3>
                    <p class="product-desc">${product.descricao || 'Sem descrição'}</p>
                    <div class="product-price">${price}</div>
                    <div class="card-actions">
                        <button class="btn-edit" onclick="editProduct('${product._id}')">Editar</button>
                        <button class="btn-delete" onclick="deleteProduct('${product._id}')">Excluir</button>
                    </div>
                </div>
            `;
            productsGrid.appendChild(card);
        });
    } catch (error) {
        showToast('Erro ao carregar produtos', true);
        console.error('Error:', error);
    }
}

// Save or Update Product
async function saveProduct(e) {
    e.preventDefault();
    
    const id = inputId.value;
    const isEditing = id !== '';
    
    const productData = {
        nome: inputNome.value,
        preco: parseFloat(inputPreco.value),
        descricao: inputDescricao.value,
        imagem: inputImagem.value
    };
    
    try {
        const url = isEditing ? `${API_URL}/${id}` : API_URL;
        const method = isEditing ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });
        
        if (response.ok) {
            closeModal();
            fetchProducts();
            showToast(isEditing ? 'Produto atualizado com sucesso!' : 'Produto adicionado com sucesso!');
        } else {
            showToast('Erro ao salvar produto', true);
        }
    } catch (error) {
        showToast('Erro ao salvar produto', true);
        console.error('Error:', error);
    }
}

// Edit Product (fetch data and show modal)
async function editProduct(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        const product = await response.json();
        
        if (response.ok) {
            modalTitle.textContent = 'Editar Produto';
            inputId.value = product._id;
            inputNome.value = product.nome || '';
            inputPreco.value = product.preco || '';
            inputDescricao.value = product.descricao || '';
            inputImagem.value = product.imagem || '';
            
            openModal();
        } else {
            showToast('Erro ao buscar produto', true);
        }
    } catch (error) {
        showToast('Erro ao buscar produto', true);
        console.error('Error:', error);
    }
}

// Delete Product
async function deleteProduct(id) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) return;
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            fetchProducts();
            showToast('Produto excluído com sucesso!');
        } else {
            showToast('Erro ao excluir produto', true);
        }
    } catch (error) {
        showToast('Erro ao excluir produto', true);
        console.error('Error:', error);
    }
}

// Modal Functions
function openModal() {
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
    productForm.reset();
    inputId.value = '';
    modalTitle.textContent = 'Adicionar Produto';
}

// Toast Function
function showToast(message, isError = false) {
    toast.textContent = message;
    
    if (isError) {
        toast.classList.add('error');
    } else {
        toast.classList.remove('error');
    }
    
    toast.className = toast.className + ' show';
    
    setTimeout(() => {
        toast.className = toast.className.replace('show', '').trim();
    }, 3000);
}

// Event Listeners
addProductBtn.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);
productForm.addEventListener('submit', saveProduct);

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Initial load
document.addEventListener('DOMContentLoaded', fetchProducts);
