/**
 * Main Application Logic for AI Command Center
 */

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

/**
 * Toast Notification Utility
 */
const Toast = {
    container: null,
    init() { this.container = document.getElementById('toastContainer'); },
    show(message, type = 'info') {
        if (!this.container) this.init();
        const icons = { success: '✓', error: '✗', info: 'ℹ', warning: '⚠' };
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ'}</span><span>${message}</span>`;
        this.container.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }
};

const App = {
    personas: {},
    activePersonaId: 'dashboard',
    chatHistories: {}, // per-persona history
    activeUploads: {}, // per-persona file uploads: { fileIds: [], fileNames: [], totalWords: 0 }

    // Per-persona quick action prompts
    promptTemplates: {
        study_mentor: [
            { icon: '$', text: 'explain --simple' },
            { icon: '$', text: 'generate --practice-problems' },
            { icon: '$', text: 'quiz --topic' },
            { icon: '$', text: 'summarize --key-concepts' }
        ],
        code_reviewer: [
            { icon: '$', text: 'review --bugs' },
            { icon: '$', text: 'scan --security' },
            { icon: '$', text: 'audit --performance' },
            { icon: '$', text: 'lint --style' }
        ],
        code_colleague: [
            { icon: '$', text: 'build --rest-api' },
            { icon: '$', text: 'refactor --function' },
            { icon: '$', text: 'test --unit' },
            { icon: '$', text: 'design --data-model' }
        ],
        document_analyzer: [
            { icon: '$', text: 'summarize --document' },
            { icon: '$', text: 'extract --key-findings' },
            { icon: '$', text: 'query --open-questions' },
            { icon: '$', text: 'generate --action-items' }
        ],
        resume_reviewer: [
            { icon: '$', text: 'improve --bullet-points' },
            { icon: '$', text: 'tailor --tech-role' },
            { icon: '$', text: 'check --ats' },
            { icon: '$', text: 'strengthen --weak-sections' }
        ],
        research_assistant: [
            { icon: '$', text: 'compare --sources' },
            { icon: '$', text: 'find --contradictions' },
            { icon: '$', text: 'map --arguments' },
            { icon: '$', text: 'generate --lit-review' }
        ]
    },

    async init() {
        // Initialize Components
        ChatComponent.init(document.getElementById('chatStream'));
        StructuredComponent.init(
            document.getElementById('structuredCanvas'),
            document.getElementById('structuredResults')
        );
        UploadComponent.init({
            zoneEl: document.getElementById('uploadZone'),
            fileInputEl: document.getElementById('fileInput'),
            attachedCardEl: document.getElementById('attachedFileCard'),
            fileNameEl: document.getElementById('fileName'),
            fileStatsEl: document.getElementById('fileStats'),
            removeBtnEl: document.getElementById('removeFileBtn'),
            onFileUploaded: (responses) => {
                const totalWords = responses.reduce((acc, curr) => acc + curr.word_count, 0);
                this.activeUploads[this.activePersonaId] = {
                    fileIds: responses.map(r => r.file_id),
                    fileNames: responses.map(r => r.filename),
                    totalWords: totalWords
                };
            },
            onFileRemoved: () => {
                this.activeUploads[this.activePersonaId] = null;
            }
        });

        // Load Personas
        await this.loadPersonas();

        // Restore chat histories from localStorage
        this.loadHistoriesFromStorage();

        // Bind DOM Events
        this.bindEvents();

        // Select initial default persona
        this.selectPersona(this.activePersonaId);
    },

    async loadPersonas() {
        try {
            const list = await API.getPersonas();
            list.forEach(p => {
                this.personas[p.id] = p;
                this.chatHistories[p.id] = [];
            });
            this.renderDashboardCards(list);
        } catch (e) {
            console.error('Failed to load personas:', e);
        }
    },

    renderDashboardCards(personas) {
        const gridEl = document.getElementById('personaGrid');
        if (!gridEl) return;

        // Change the class to match the new tabular structure
        gridEl.className = 'persona-table';

        gridEl.innerHTML = `
            <div class="table-header">
                <div class="th-col">PERSONA</div>
                <div class="th-col">DESCRIPTION</div>
                <div class="th-col">MODE</div>
                <div class="th-col">ACTION</div>
            </div>
            ${personas.map(p => `
                <div class="table-row" onclick="App.selectPersona('${p.id}')">
                    <div class="td-col title-col">
                        <span class="icon-terminal">>_</span>
                        <span class="persona-name">${p.display_name}</span>
                    </div>
                    <div class="td-col desc-col">${p.description}</div>
                    <div class="td-col mode-col">
                        <span class="mode-tag ${p.output_mode === 'json_schema' ? 'json' : 'stream'}">
                            ${p.output_mode === 'json_schema' ? 'JSON' : 'STREAM'}
                        </span>
                    </div>
                    <div class="td-col action-col">
                        <span class="launch-btn">[ LAUNCH ]</span>
                    </div>
                </div>
            `).join('')}
        `;
    },

    bindEvents() {
        // Sidebar Navigation
        const sidebarNav = document.getElementById('sidebarNav');
        if (sidebarNav) {
            sidebarNav.addEventListener('click', (e) => {
                const item = e.target.closest('.sidebar-item');
                if (item && item.dataset.persona) {
                    this.selectPersona(item.dataset.persona);
                }
            });
        }

        // Send Button
        const sendBtn = document.getElementById('sendBtn');
        const userInput = document.getElementById('userInput');
        const wordCountDisplay = document.getElementById('wordCountDisplay');

        if (sendBtn && userInput) {
            sendBtn.addEventListener('click', () => this.handleSendMessage());

            userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSendMessage();
                }
            });

            if (wordCountDisplay) {
                userInput.addEventListener('input', () => {
                    const text = userInput.value.trim();
                    const words = text ? text.split(/\s+/).length : 0;
                    const chars = text.length;
                    wordCountDisplay.textContent = `${words} word${words !== 1 ? 's' : ''} | ${chars} char${chars !== 1 ? 's' : ''}`;
                });
            }
        }

        // Clear Memory Button
        const clearBtn = document.getElementById('clearSessionBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                if (this.activePersonaId && this.activePersonaId !== 'dashboard') {
                    this.chatHistories[this.activePersonaId] = [];
                    this.activeUploads[this.activePersonaId] = null;
                    this.saveHistoriesToStorage();
                    ChatComponent.clear();
                    StructuredComponent.clear();
                    UploadComponent.clearFile();
                    this.selectPersona(this.activePersonaId);
                    Toast.show(`Session cleared for ${this.personas[this.activePersonaId]?.display_name || 'persona'}`, 'success');
                }
            });
        }

        // Export Chat Button
        const exportBtn = document.getElementById('exportChatBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportChatAsMarkdown());
        }
        
        // Theme Toggle Button (Dark -> Light -> Neon)
        const themeBtn = document.getElementById('themeToggleBtn');
        if (themeBtn) {
            const updateThemeIcon = (theme) => {
                const label = document.getElementById('themeLabel');
                if (label) label.textContent = `theme: ${theme}`;
            };
            
            // Set initial icon
            updateThemeIcon(document.documentElement.getAttribute('data-theme') || 'dark');
            
            themeBtn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
                let newTheme = 'dark';
                if (currentTheme === 'dark') newTheme = 'light';
                else if (currentTheme === 'light') newTheme = 'neon';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                updateThemeIcon(newTheme);
                localStorage.setItem('theme', newTheme);
                
                // Swap highlight.js theme
                const hljsLink = document.getElementById('hljs-theme');
                if (hljsLink) {
                    hljsLink.href = newTheme === 'light'
                        ? 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css'
                        : 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/tokyo-night-dark.min.css';
                }
            });
        }
    },

    selectPersona(personaId) {
        this.activePersonaId = personaId;

        // Highlight Active Sidebar Item
        const items = document.querySelectorAll('.sidebar-item');
        items.forEach(item => {
            if (item.dataset.persona === personaId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        const dashboardView = document.getElementById('dashboardView');
        const workspaceView = document.getElementById('workspaceView');

        if (personaId === 'dashboard') {
            if (dashboardView) dashboardView.classList.add('active');
            if (workspaceView) workspaceView.classList.remove('active');
            return;
        }

        if (dashboardView) dashboardView.classList.remove('active');
        if (workspaceView) workspaceView.classList.add('active');

        const persona = this.personas[personaId];
        if (!persona) return;

        // Update Workspace Header if present
        const titleEl = document.getElementById('personaTitle');
        if (titleEl) titleEl.textContent = persona.display_name;
        
        const descEl = document.getElementById('personaDesc');
        if (descEl) descEl.textContent = persona.description;

        const badge = document.getElementById('personaBadge');
        if (badge) {
            badge.textContent = persona.output_mode === 'json_schema' ? 'Structured Audit' : 'Dialogue Stream';
            badge.className = `persona-pill ${persona.output_mode === 'json_schema' ? 'json' : ''}`;
        }

        // Toggle Upload Zone & Restore State
        const uploadZone = document.getElementById('uploadZone');
        if (persona.requires_upload) {
            uploadZone.classList.remove('hidden');
            const state = this.activeUploads[personaId];
            if (state) {
                UploadComponent.setFiles(state.fileIds, state.fileNames, state.totalWords);
            } else {
                UploadComponent.clearFile();
            }
        } else {
            uploadZone.classList.add('hidden');
            UploadComponent.clearFile();
        }

        // Toggle Canvas Modes
        const chatStream = document.getElementById('chatStream');
        const structuredCanvas = document.getElementById('structuredCanvas');
        const emptyStateView = document.getElementById('emptyStateView');
        
        const history = this.chatHistories[personaId] || [];
        
        if (history.length === 0) {
            document.getElementById('emptyStateIcon').textContent = '[>_]';
            document.getElementById('emptyStateTitle').textContent = `session: ${personaId}`;
            document.getElementById('emptyStateDesc').textContent = `// ${persona.description}`;

            // Render Prompt Templates
            const quickActionsEl = document.getElementById('quickActions');
            const templates = this.promptTemplates[personaId] || [];
            quickActionsEl.innerHTML = templates.map(t =>
                `<button class="quick-action-btn" data-prompt="${t.text}"><span class="qa-icon">${t.icon}</span> ${t.text}</button>`
            ).join('');
            quickActionsEl.querySelectorAll('.quick-action-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.getElementById('userInput').value = btn.dataset.prompt;
                    document.getElementById('userInput').focus();
                });
            });
            
            emptyStateView.classList.remove('hidden');
            chatStream.classList.add('hidden');
            structuredCanvas.classList.add('hidden');
        } else {
            emptyStateView.classList.add('hidden');
            if (persona.output_mode === 'json_schema') {
                chatStream.classList.add('hidden');
                structuredCanvas.classList.remove('hidden');
            } else {
                chatStream.classList.remove('hidden');
                structuredCanvas.classList.add('hidden');
            }
        }
    },

    async handleSendMessage() {
        const userInputEl = document.getElementById('userInput');
        const message = userInputEl.value.trim();

        if (!message) return;
        if (this.activePersonaId === 'dashboard') {
            Toast.show('Please select a persona first', 'warning');
            return;
        }

        const persona = this.personas[this.activePersonaId];
        const fileIds = UploadComponent.getFileIds();

        if (persona.requires_upload && fileIds.length === 0 && this.activePersonaId === 'document_analyzer') {
            Toast.show('Document Analyzer requires at least one document upload', 'warning');
            return;
        }

        // Clear input box
        userInputEl.value = '';
        const wordCountDisplay = document.getElementById('wordCountDisplay');
        if (wordCountDisplay) wordCountDisplay.textContent = '0 words | 0 chars';
        
        // Disable input while streaming
        const sendBtn = document.getElementById('sendBtn');
        userInputEl.disabled = true;
        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.5';

        const history = this.chatHistories[this.activePersonaId] || [];

        // Hide empty state and show correct canvas
        document.getElementById('emptyStateView').classList.add('hidden');
        if (persona.output_mode === 'json_schema') {
            document.getElementById('structuredCanvas').classList.remove('hidden');
        } else {
            document.getElementById('chatStream').classList.remove('hidden');
        }

        if (persona.output_mode === 'json_schema') {
            // Structured Canvas Mode
            StructuredComponent.clear();
            const resultsEl = document.getElementById('structuredResults');
            resultsEl.innerHTML = '<div class="audit-section"><p class="issue-meta">⏳ Running structured AI audit...</p></div>';

            let fullOutput = '';
            await API.streamChat(
                this.activePersonaId,
                { message, history, file_ids: fileIds },
                (token) => {
                    fullOutput += token;
                },
                (err) => {
                    resultsEl.innerHTML = `<div class="audit-section"><p style="color:var(--accent-rose)">Error: ${err}</p></div>`;
                    // Re-enable input
                    userInputEl.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.style.opacity = '1';
                },
                () => {
                    StructuredComponent.renderRawJSON(fullOutput, this.activePersonaId);
                    // Re-enable input
                    userInputEl.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.style.opacity = '1';
                }
            );

            // Record history
            history.push({ role: 'user', content: message });
            history.push({ role: 'assistant', content: fullOutput });
        } else {
            // Freeform Chat Stream Mode
            ChatComponent.appendUserMessage(message);
            const contentEl = ChatComponent.createAssistantBubble();

            let fullOutput = '';
            await API.streamChat(
                this.activePersonaId,
                { message, history, file_ids: fileIds },
                (token) => {
                    fullOutput += token;
                    ChatComponent.appendToken(contentEl, token);
                },
                (err) => {
                    ChatComponent.appendToken(contentEl, `\n[Error: ${err}]`);
                    ChatComponent.finalizeBubble(contentEl);
                    // Re-enable input
                    userInputEl.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.style.opacity = '1';
                },
                () => {
                    ChatComponent.finalizeBubble(contentEl);
                    // Re-enable input
                    userInputEl.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.style.opacity = '1';
                    
                    // Record history
                    history.push({ role: 'user', content: message });
                    history.push({ role: 'assistant', content: fullOutput });
                    this.saveHistoriesToStorage();
                }
            );
        }
    },

    // --- Chat History Persistence ---
    saveHistoriesToStorage() {
        try {
            const data = {};
            for (const [pid, hist] of Object.entries(this.chatHistories)) {
                // Keep only last 20 messages per persona to avoid quota issues
                data[pid] = hist.slice(-20);
            }
            localStorage.setItem('acc_chat_histories', JSON.stringify(data));
        } catch (e) {
            console.warn('Could not save chat histories:', e);
        }
    },

    loadHistoriesFromStorage() {
        try {
            const stored = localStorage.getItem('acc_chat_histories');
            if (stored) {
                const data = JSON.parse(stored);
                for (const [pid, hist] of Object.entries(data)) {
                    if (this.chatHistories[pid] !== undefined) {
                        this.chatHistories[pid] = hist;
                    }
                }
            }
        } catch (e) {
            console.warn('Could not load chat histories:', e);
        }
    },

    // --- Export Chat as Markdown ---
    exportChatAsMarkdown() {
        if (this.activePersonaId === 'dashboard') {
            Toast.show('Select a persona to export its chat', 'warning');
            return;
        }
        const history = this.chatHistories[this.activePersonaId] || [];
        if (history.length === 0) {
            Toast.show('No conversation to export', 'info');
            return;
        }
        const persona = this.personas[this.activePersonaId];
        let md = `# ${persona.display_name} — Chat Export\n`;
        md += `> Exported on ${new Date().toLocaleString()}\n\n---\n\n`;
        history.forEach(msg => {
            const label = msg.role === 'user' ? '**You**' : `**${persona.display_name}**`;
            md += `### ${label}\n\n${msg.content}\n\n---\n\n`;
        });
        const blob = new Blob([md], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.activePersonaId}_chat_${Date.now()}.md`;
        a.click();
        URL.revokeObjectURL(url);
        Toast.show('Chat exported as Markdown', 'success');
    }
};
