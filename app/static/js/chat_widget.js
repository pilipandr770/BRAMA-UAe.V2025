// BRAMA-UAe.V2025 - Chat Widget Implementation

class ChatWidget {
    constructor() {
        this.isOpen = false;
        this.isInitialized = false;
        this.messages = [];
        this.init();
    }

    init() {
        if (this.isInitialized) return;
        
        this.createChatHTML();
        this.bindEvents();
        this.isInitialized = true;
    }

    createChatHTML() {
        // Create chat toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'chat-toggle';
        toggleBtn.innerHTML = '💬';
        toggleBtn.setAttribute('aria-label', 'Toggle chat');
        document.body.appendChild(toggleBtn);

        // Create chat widget
        const chatWidget = document.createElement('div');
        chatWidget.className = 'chat-widget';
        chatWidget.innerHTML = `
            <div class="chat-header">
                <span>🇺🇦 BRAMA-UAe Assistant</span>
                <button class="chat-close" aria-label="Close chat">×</button>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="chat-message bot-message">
                    <div class="message-content">
                        Привіт! Я помічник BRAMA-UAe. Задавайте питання українською або німецькою мовою.<br>
                        <small>Hallo! Ich bin der BRAMA-UAe Assistent. Stellen Sie Fragen auf Ukrainisch oder Deutsch.</small>
                    </div>
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" placeholder="Введіть повідомлення... / Nachricht eingeben..." maxlength="500">
                <button class="chat-send">📤</button>
            </div>
        `;
        
        document.body.appendChild(chatWidget);
        
        this.toggleBtn = toggleBtn;
        this.chatWidget = chatWidget;
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = chatWidget.querySelector('.chat-input');
        this.chatSend = chatWidget.querySelector('.chat-send');
        this.chatClose = chatWidget.querySelector('.chat-close');
    }

    bindEvents() {
        // Toggle chat
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        this.chatClose.addEventListener('click', () => this.closeChat());

        // Send message
        this.chatSend.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Close chat when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isOpen && 
                !this.chatWidget.contains(e.target) && 
                !this.toggleBtn.contains(e.target)) {
                this.closeChat();
            }
        });
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        this.isOpen = true;
        this.chatWidget.classList.add('open');
        this.toggleBtn.style.display = 'none';
        this.chatInput.focus();
    }

    closeChat() {
        this.isOpen = false;
        this.chatWidget.classList.remove('open');
        this.toggleBtn.style.display = 'block';
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        this.chatInput.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.hideTyping();
            
            // Add bot response
            this.addMessage(data.response || 'Вибачте, не можу відповісти зараз.', 'bot');
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTyping();
            this.addMessage('Технічна помилка. Спробуйте пізніше. / Technischer Fehler. Versuchen Sie es später.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString('uk-UA', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${this.formatMessage(text)}
                <div class="message-time">${timestamp}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store message
        this.messages.push({ text, sender, timestamp });
    }

    formatMessage(text) {
        // Basic text formatting
        return text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot-message typing';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <span class="typing-dots">
                    <span>●</span><span>●</span><span>●</span>
                </span>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Additional chat message styles
const chatStyles = `
<style>
.chat-message {
    margin: 1rem 0;
    display: flex;
    align-items: flex-start;
}

.user-message {
    justify-content: flex-end;
}

.bot-message {
    justify-content: flex-start;
}

.message-content {
    max-width: 80%;
    padding: 0.75rem;
    border-radius: 15px;
    position: relative;
    word-wrap: break-word;
}

.user-message .message-content {
    background: var(--primary-color);
    color: white;
    border-bottom-right-radius: 5px;
}

.bot-message .message-content {
    background: white;
    color: var(--dark-color);
    border: 1px solid #e0e0e0;
    border-bottom-left-radius: 5px;
}

.message-time {
    font-size: 0.7rem;
    opacity: 0.7;
    margin-top: 0.25rem;
}

.typing .message-content {
    background: #f0f0f0;
    padding: 0.5rem 1rem;
}

.typing-dots {
    display: inline-flex;
    gap: 0.2rem;
}

.typing-dots span {
    animation: typingBounce 1.4s infinite ease-in-out;
    font-size: 1.2rem;
    color: var(--primary-color);
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }
.typing-dots span:nth-child(3) { animation-delay: 0s; }

@keyframes typingBounce {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

/* Responsive chat */
@media (max-width: 480px) {
    .chat-widget {
        bottom: 0;
        right: 0;
        left: 0;
        width: 100%;
        max-height: 70vh;
        border-radius: 15px 15px 0 0;
    }
    
    .chat-toggle {
        bottom: 10px;
        right: 10px;
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
    }
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', chatStyles);

// Initialize chat widget when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is on a page where chat should be available
    if (!document.body.classList.contains('no-chat')) {
        const chatWidget = new ChatWidget();
    }
});

// Utility functions for other parts of the app
window.BRAMAUtils = {
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
            max-width: 300px;
            animation: slideUp 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    },

    // Format date for Ukrainian/German locale
    formatDate: function(date, lang = 'uk') {
        const locale = lang === 'de' ? 'de-DE' : 'uk-UA';
        return new Date(date).toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // AJAX helper for voting
    vote: function(projectId, value) {
        return fetch(`/dashboard/project/${projectId}/vote/${value}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    }
};

// Add fade-out animation
const fadeOutStyle = `
@keyframes fadeOut {
    to {
        opacity: 0;
        transform: translateX(100%);
    }
}
`;
document.head.insertAdjacentHTML('beforeend', `<style>${fadeOutStyle}</style>`);