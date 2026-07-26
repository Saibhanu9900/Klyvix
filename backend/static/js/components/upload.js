/**
 * PDF File Upload Component
 */

const UploadComponent = {
    zoneEl: null,
    fileInputEl: null,
    attachedCardEl: null,
    fileNameEl: null,
    fileStatsEl: null,
    removeBtnEl: null,

    currentFileIds: [],
    currentFileNames: [],

    init({ zoneEl, fileInputEl, attachedCardEl, fileNameEl, fileStatsEl, removeBtnEl, onFileUploaded, onFileRemoved }) {
        this.zoneEl = zoneEl;
        this.fileInputEl = fileInputEl;
        this.attachedCardEl = attachedCardEl;
        this.fileNameEl = fileNameEl;
        this.fileStatsEl = fileStatsEl;
        this.removeBtnEl = removeBtnEl;

        this.onFileUploaded = onFileUploaded;
        this.onFileRemoved = onFileRemoved;

        this.bindEvents();
    },

    bindEvents() {
        if (!this.fileInputEl) return;

        this.fileInputEl.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                this.handleFileUpload(e.target.files);
            }
        });

        if (this.removeBtnEl) {
            this.removeBtnEl.addEventListener('click', () => {
                this.clearFile();
                if (this.onFileRemoved) this.onFileRemoved();
            });
        }
    },

    async handleFileUpload(files) {
        if (!files || files.length === 0) {
            return;
        }

        try {
            if (this.zoneEl) this.zoneEl.style.opacity = '0.5';

            const responses = await API.uploadDocuments(files);
            
            this.currentFileIds = responses.map(r => r.file_id);
            this.currentFileNames = responses.map(r => r.filename);

            if (this.fileNameEl) {
                this.fileNameEl.textContent = this.currentFileNames.join(', ');
            }
            if (this.fileStatsEl) {
                const totalWords = responses.reduce((acc, curr) => acc + curr.word_count, 0);
                this.fileStatsEl.textContent = `${totalWords} words total`;
            }

            if (this.attachedCardEl) this.attachedCardEl.classList.remove('hidden');

            if (this.onFileUploaded) this.onFileUploaded(responses);
        } catch (err) {
            Toast.show(`Upload failed: ${err.message}`, 'error');
        } finally {
            if (this.zoneEl) this.zoneEl.style.opacity = '1';
        }
    },

    clearFile() {
        this.currentFileIds = [];
        this.currentFileNames = [];
        if (this.fileInputEl) this.fileInputEl.value = '';
        if (this.attachedCardEl) this.attachedCardEl.classList.add('hidden');
    },

    setFiles(fileIds, fileNames, totalWords) {
        this.currentFileIds = fileIds || [];
        this.currentFileNames = fileNames || [];
        
        if (this.currentFileIds.length > 0) {
            if (this.fileNameEl) {
                this.fileNameEl.textContent = this.currentFileNames.join(', ');
            }
            if (this.fileStatsEl) {
                this.fileStatsEl.textContent = `${totalWords || 0} words total`;
            }
            if (this.attachedCardEl) this.attachedCardEl.classList.remove('hidden');
        } else {
            this.clearFile();
        }
    },

    getFileIds() {
        return this.currentFileIds;
    }
};
