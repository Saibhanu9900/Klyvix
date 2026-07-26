/**
 * Structured Output Component (Code Reviewer & Resume Reviewer)
 */

const StructuredComponent = {
    canvasEl: null,
    resultsEl: null,

    init(canvasEl, resultsEl) {
        this.canvasEl = canvasEl;
        this.resultsEl = resultsEl;
    },

    clear() {
        if (this.resultsEl) {
            this.resultsEl.innerHTML = '';
        }
    },

    renderRawJSON(jsonText, personaId) {
        try {
            // Clean up possible markdown code blocks ```json ... ```
            let cleanText = jsonText.trim();
            if (cleanText.startsWith('```json')) {
                cleanText = cleanText.replace(/^```json/, '').replace(/```$/, '').trim();
            } else if (cleanText.startsWith('```')) {
                cleanText = cleanText.replace(/^```/, '').replace(/```$/, '').trim();
            }

            const data = JSON.parse(cleanText);
            this.clear();

            if (personaId === 'code_reviewer') {
                this.renderCodeReview(data);
            } else if (personaId === 'resume_reviewer') {
                this.renderResumeReview(data);
            } else {
                this.renderGenericJSON(data);
            }
        } catch (e) {
            console.error('Failed to parse structured JSON response:', e, jsonText);
            this.resultsEl.innerHTML = `
                <div class="audit-section">
                    <h4 class="section-header-title">Raw Response</h4>
                    <div class="code-snippet">${this.escapeHtml(jsonText)}</div>
                </div>
            `;
        }
    },

    renderCodeReview(data) {
        let html = '';

        if (data.language_detected || data.summary || data.overall_quality_rating) {
            html += `
                <div class="audit-section">
                    <h4 class="section-header-title">📌 Overview (${this.escapeHtml(data.language_detected || 'Code')}${data.language_confidence ? ` - ${this.escapeHtml(data.language_confidence)}` : ''})</h4>
                    ${data.overall_quality_rating ? `<div class="issue-meta"><strong>Quality Rating:</strong> ${this.escapeHtml(data.overall_quality_rating)}</div>` : ''}
                    <p class="workspace-desc">${this.escapeHtml(data.summary || 'Code audit complete.')}</p>
                </div>
            `;
        }

        html += this.renderIssueCategory('🐛 Bugs & Correctness', data.bugs_and_correctness, 'section-bugs');
        html += this.renderIssueCategory('🛡️ Security Vulnerabilities', data.security, 'section-security');
        html += this.renderIssueCategory('⚡ Performance', data.performance, 'section-performance');
        html += this.renderIssueCategory('🎨 Style & Best Practices', data.style_and_best_practices, 'section-style');

        this.resultsEl.innerHTML = html;
    },

    renderIssueCategory(title, issues, borderClass) {
        if (!issues || issues.length === 0) {
            return `
                <div class="audit-section ${borderClass}">
                    <h4 class="section-header-title">${title}</h4>
                    <p class="issue-meta">✓ No significant issues found in this category.</p>
                </div>
            `;
        }

        let itemsHtml = issues.map(item => `
            <div class="issue-card">
                <div class="issue-title">${this.escapeHtml(item.issue || 'Issue')}</div>
                ${item.location ? `<div class="issue-meta"><strong>Location:</strong> ${this.escapeHtml(item.location)}</div>` : ''}
                <div class="issue-meta"><strong>Why it matters:</strong> ${this.escapeHtml(item.why_it_matters || '')}</div>
                ${item.suggested_fix ? `<div class="code-snippet">Suggested Fix:\n${this.escapeHtml(item.suggested_fix)}</div>` : ''}
            </div>
        `).join('');

        return `
            <div class="audit-section ${borderClass}">
                <h4 class="section-header-title">${title} (${issues.length})</h4>
                ${itemsHtml}
            </div>
        `;
    },

    renderResumeReview(data) {
        let html = '';

        // Overall Assessment
        if (data.overall_assessment) {
            html += `
                <div class="audit-section">
                    <h4 class="section-header-title">📌 Overall Assessment</h4>
                    <p class="workspace-desc">${this.escapeHtml(data.overall_assessment)}</p>
                </div>
            `;
        }

        // Priority Actions
        if (data.priority_actions && data.priority_actions.length > 0) {
            const list = data.priority_actions.map(a => `<li>${this.escapeHtml(a)}</li>`).join('');
            html += `
                <div class="audit-section" style="border-left: 3px solid #f43f5e;">
                    <h4 class="section-header-title">🚨 Priority Actions</h4>
                    <ul style="padding-left:1.25rem; line-height:1.7;">${list}</ul>
                </div>
            `;
        }

        // Strengths
        if (data.strengths && data.strengths.length > 0) {
            const list = data.strengths.map(s => `<li>${this.escapeHtml(s)}</li>`).join('');
            html += `
                <div class="audit-section section-strengths">
                    <h4 class="section-header-title">🌟 Key Strengths</h4>
                    <ul style="padding-left:1.25rem; line-height:1.7;">${list}</ul>
                </div>
            `;
        }

        // Gaps
        if (data.gaps && data.gaps.length > 0) {
            const list = data.gaps.map(g => `<li>${this.escapeHtml(g)}</li>`).join('');
            html += `
                <div class="audit-section section-gaps">
                    <h4 class="section-header-title">⚠️ Areas for Improvement (Gaps)</h4>
                    <ul style="padding-left:1.25rem; line-height:1.7;">${list}</ul>
                </div>
            `;
        }

        // Suggestions with Before/After Diff
        if (data.suggestions && data.suggestions.length > 0) {
            const diffs = data.suggestions.map(s => `
                <div class="issue-card">
                    <div class="issue-meta"><strong>Rationale:</strong> ${this.escapeHtml(s.why || '')}</div>
                    <div class="diff-container">
                        <div class="diff-box original">
                            <div class="diff-label">Original Bullet</div>
                            <div>${this.escapeHtml(s.original || '')}</div>
                        </div>
                        <div class="diff-box improved">
                            <div class="diff-label">Improved Rewrite</div>
                            <div>${this.escapeHtml(s.improved || '')}</div>
                        </div>
                    </div>
                </div>
            `).join('');

            html += `
                <div class="audit-section section-suggestions">
                    <h4 class="section-header-title">💡 Concrete Actionable Suggestions</h4>
                    ${diffs}
                </div>
            `;
        }

        this.resultsEl.innerHTML = html;
    },

    renderGenericJSON(data) {
        this.resultsEl.innerHTML = `
            <div class="audit-section">
                <h4 class="section-header-title">Analysis Results</h4>
                <div class="code-snippet">${this.escapeHtml(JSON.stringify(data, null, 2))}</div>
            </div>
        `;
    },

    escapeHtml(str) {
        if (typeof str !== 'string') return String(str);
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
};
