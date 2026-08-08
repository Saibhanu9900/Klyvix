/**
 * API Communication Layer for Klyvix
 */

const API = {
    /**
     * Gets or creates a JWT token for the session
     */
    async getToken() {
        let token = localStorage.getItem('jwt_token');
        if (token) return token;
        
        // Auto-register a temporary user for testing Phase 1
        const email = `test_${Math.random().toString(36).substring(7)}@example.com`;
        const res = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: 'testpassword' })
        });
        
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('jwt_token', data.access_token);
            return data.access_token;
        }
        return null;
    },

    /**
     * Fetches persona list from backend
     */
    async getPersonas() {
        const res = await fetch('/api/personas');
        if (!res.ok) throw new Error('Failed to fetch personas list');
        return await res.json();
    },

    /**
     * Uploads PDF document to backend
     */
    async uploadDocuments(files) {
        const token = await this.getToken();
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        const res = await fetch('/api/upload', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || 'Document upload failed');
        }
        return await res.json();
    },

    /**
     * Sends streaming chat request via SSE / ReadableStream
     */
    async streamChat(personaId, payload, onChunk, onError, onComplete) {
        try {
            const token = await this.getToken();
            const res = await fetch(`/api/chat/${personaId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Chat request failed');
            }

            const reader = res.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n\n');
                buffer = lines.pop(); // keep last incomplete line

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.substring(6).trim();
                        if (dataStr === '[DONE]') {
                            if (onComplete) onComplete();
                            return;
                        }
                        try {
                            const parsed = JSON.parse(dataStr);
                            if (parsed.error) {
                                if (onError) onError(parsed.error);
                                return;
                            }
                            if (parsed.token && onChunk) {
                                onChunk(parsed.token);
                            }
                        } catch (e) {
                            console.error('SSE JSON parse error:', e, dataStr);
                        }
                    }
                }
            }

            if (onComplete) onComplete();
        } catch (err) {
            if (onError) onError(err.message);
        }
    }
};
