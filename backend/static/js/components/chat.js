/**
 * Terminal Chat Stream Component
 * Renders user input as terminal commands ($ ...) and assistant output as stdout
 */

const ChatComponent = {
    container: null,

    init(containerEl) {
        this.container = containerEl;
        
        // Initialize Marked + KaTeX if available
        if (window.marked && window.markedKatex) {
            marked.use(window.markedKatex({
                throwOnError: false,
                nonStandard: true
            }));
        }
    },

    clear() {
        if (!this.container) return;
        this.container.innerHTML = '';
    },

    appendUserMessage(text) {
        const welcome = this.container.querySelector('.welcome-message');
        if (welcome) welcome.remove();

        // Render as a terminal command line
        const cmdBlock = document.createElement('div');
        cmdBlock.className = 'terminal-cmd';
        
        // Show raw text as command, no markdown rendering for user input
        const escapedText = this.escapeHtml(text);
        const lines = escapedText.split('\n');
        
        if (lines.length === 1) {
            cmdBlock.innerHTML = `<span class="prompt-symbol">$</span> <span class="cmd-text">${lines[0]}</span>`;
        } else {
            // Multi-line: first line with $, subsequent lines with >
            cmdBlock.innerHTML = lines.map((line, i) => {
                const prefix = i === 0 ? '$' : '>';
                return `<span class="prompt-symbol">${prefix}</span> <span class="cmd-text">${line}</span>`;
            }).join('\n');
        }
        
        this.container.appendChild(cmdBlock);
        this.scrollToBottom();
    },

    createAssistantBubble() {
        const welcome = this.container.querySelector('.welcome-message');
        if (welcome) welcome.remove();

        // Processing indicator (like a terminal spinner)
        const processingLine = document.createElement('div');
        processingLine.className = 'terminal-processing';
        processingLine.innerHTML = `<span class="processing-text">[processing...]</span>`;
        this.container.appendChild(processingLine);

        // Output block
        const outputBlock = document.createElement('div');
        outputBlock.className = 'terminal-output';
        
        const contentEl = document.createElement('div');
        contentEl.className = 'output-content markdown-body';
        outputBlock.appendChild(contentEl);

        // Copy button (hidden until finalized)
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-output-btn hidden';
        copyBtn.title = 'Copy output';
        copyBtn.textContent = '[copy]';
        outputBlock.appendChild(copyBtn);

        this.container.appendChild(outputBlock);
        this.scrollToBottom();
        
        contentEl.dataset.raw = '';
        contentEl._processingLine = processingLine;

        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(contentEl.dataset.raw).then(() => {
                const orig = copyBtn.textContent;
                copyBtn.textContent = '[copied ✓]';
                copyBtn.style.color = 'var(--accent-green)';
                setTimeout(() => { 
                    copyBtn.textContent = orig;
                    copyBtn.style.color = '';
                }, 2000);
            });
        });

        return contentEl;
    },

    finalizeBubble(contentEl) {
        // Remove processing indicator
        if (contentEl._processingLine) {
            contentEl._processingLine.remove();
        }
        // Show copy button
        const copyBtn = contentEl.parentElement.querySelector('.copy-output-btn');
        if (copyBtn) copyBtn.classList.remove('hidden');
        this.highlightCodeBlocks(contentEl);
    },

    appendToken(contentEl, token) {
        contentEl.dataset.raw += token;
        
        if (window.marked) {
            const parsed = marked.parse(contentEl.dataset.raw);
            contentEl.innerHTML = window.DOMPurify ? DOMPurify.sanitize(parsed, { ADD_ATTR: ['class', 'target', 'aria-hidden', 'style'], USE_PROFILES: { html: true, mathMl: true } }) : parsed;
        } else {
            contentEl.textContent = contentEl.dataset.raw;
        }
        this.highlightCodeBlocks(contentEl);
        this.scrollToBottom();
    },

    highlightCodeBlocks(el) {
        if (!window.hljs) return;
        el.querySelectorAll('pre code:not(.hljs)').forEach(block => {
            hljs.highlightElement(block);
            
            const pre = block.parentElement;
            if (pre && pre.tagName === 'PRE' && !pre.querySelector('.copy-code-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-code-btn';
                copyBtn.textContent = 'Copy';
                copyBtn.title = 'Copy code to clipboard';
                
                copyBtn.addEventListener('click', () => {
                    navigator.clipboard.writeText(block.textContent).then(() => {
                        const orig = copyBtn.textContent;
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => { 
                            copyBtn.textContent = orig;
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
                });
                
                pre.appendChild(copyBtn);
            }
        });
    },

    scrollToBottom() {
        if (!this.container) return;
        const canvas = this.container.closest('.canvas-container');
        if (canvas) canvas.scrollTop = canvas.scrollHeight;
    },

    escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
};
