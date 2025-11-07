/**
 * Advertising Widget - Muestra publicidad de productos tecnológicos
 */

class AdvertisingWidget {
    constructor() {
        this.adContainer = null;
        this.refreshInterval = 30000; // 30 segundos
        this.translations = {};
        this.init();
    }

    async init() {
        // Cargar traducciones primero
        await this.loadTranslations();
        
        await this.loadAd();
        
        // Solo configurar el intervalo si hay contenido
        if (this.adContainer) {
            setInterval(() => {
                this.loadAd();
            }, this.refreshInterval);
        }
    }

    async loadTranslations() {
        try {
            const response = await fetch('/api/translations/');
            const data = await response.json();
            
            if (data.success) {
                this.translations = data.translations;
            } else {
                // Fallback translations
                this.translations = {
                    'ADS_TITLE': 'Publicidad',
                    'ADS_VIEW_DETAILS': 'Ver detalles',
                    'ADS_NO_DATA': 'Publicidad no disponible'
                };
            }
        } catch (error) {
            console.error('Error loading translations:', error);
            // Fallback translations
            this.translations = {
                'ADS_TITLE': 'Publicidad',
                'ADS_VIEW_DETAILS': 'Ver detalles',
                'ADS_NO_DATA': 'Publicidad no disponible'
            };
        }
    }

    async loadAd() {
        try {
            const response = await fetch('/api/ads/');
            const data = await response.json();
            
            if (data.success && data.ad_products && data.ad_products.length > 0) {
                if (!this.adContainer) {
                    this.createAdContainer();
                }
                this.displayAds(data.ad_products, data.company);
            } else {
                // No hay datos disponibles, remover la sección si existe
                this.removeAdContainer();
                console.log('No advertising data available');
            }
        } catch (error) {
            console.error('Error loading advertisement:', error);
            // Error al cargar, remover la sección si existe
            this.removeAdContainer();
        }
    }

    createAdContainer() {
        // Solo crear si no existe ya
        if (this.adContainer) return;
        
        // Buscar el footer para insertar la publicidad antes de él
        const footer = document.querySelector('footer');
        if (footer) {
            // Crear contenedor de publicidad
            this.adContainer = document.createElement('section');
            this.adContainer.className = 'bg-gray-900 border-t border-gray-700 py-6';
            this.adContainer.id = 'tech-ad-container';
            this.adContainer.innerHTML = `
                <div class="container mx-auto px-4">
                    <div class="text-center mb-4">
                        <span class="text-xs text-gray-500 uppercase tracking-wide">${this.translations.ADS_TITLE}</span>
                    </div>
                    <div id="ad-content" class="flex justify-center">
                        <!-- Content will be loaded here -->
                    </div>
                </div>
            `;
            
            // Insertar antes del footer
            footer.parentNode.insertBefore(this.adContainer, footer);
        }
    }

    removeAdContainer() {
        if (this.adContainer) {
            this.adContainer.remove();
            this.adContainer = null;
        }
    }

    displayAds(products, company) {
        const adContent = document.getElementById('ad-content');
        if (!adContent) return;

        // Crear grid responsive para 3 productos
        const adsHTML = products.map(product => {
            const description = this.truncateDescription(product.descripcion, 80);
            
            return `
                <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow cursor-pointer"
                     onclick="window.open('${product.detail_url}', '_blank')"
                     role="button"
                     tabindex="0"
                     onkeydown="if(event.key==='Enter') window.open('${product.detail_url}', '_blank')">
                    
                    <div class="relative">
                        <img src="${product.imagen_url}" 
                             alt="${product.nombre}"
                             class="w-full h-32 object-cover"
                             onerror="this.src='https://via.placeholder.com/300x150/374151/9ca3af?text=Tech'">
                        <div class="absolute top-2 right-2 bg-blue-600 text-white text-xs px-2 py-1 rounded">
                            ${company || 'TechStore'}
                        </div>
                    </div>
                    
                    <div class="p-3">
                        <h3 class="text-white font-semibold text-sm mb-2 line-clamp-2">
                            ${product.nombre}
                        </h3>
                        <p class="text-gray-300 text-xs mb-2 line-clamp-2">
                            ${description}
                        </p>
                        <div class="flex items-center justify-between">
                            <span class="text-blue-400 text-xs font-medium">${this.translations.ADS_VIEW_DETAILS}</span>
                            <svg class="w-3 h-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                            </svg>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        adContent.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
                ${adsHTML}
            </div>
        `;
    }

    truncateDescription(text, maxLength) {
        if (!text) return '';
        
        // Limpiar caracteres de escape
        const cleanText = text.replace(/\\r\\n/g, ' ').replace(/\r\n/g, ' ').replace(/\n/g, ' ');
        
        if (cleanText.length <= maxLength) {
            return cleanText;
        }
        
        return cleanText.substring(0, maxLength).trim() + '...';
    }
}

// CSS adicional para truncar texto
const style = document.createElement('style');
style.textContent = `
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    #tech-ad-container {
        animation: slideInUp 0.5s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new AdvertisingWidget();
});
