// TipTap Editor Implementation for daygun.net
// Supports Turkish and English markdown editors with accessibility features

document.addEventListener('DOMContentLoaded', function() {
    const { Editor } = window.tiptap.core;
    const StarterKit = window.tiptap.starterKit.StarterKit;

    // Get form elements
    const contentEnTextarea = document.getElementById('id_content_en');
    const contentTrTextarea = document.getElementById('id_content_tr');
    
    if (!contentEnTextarea || !contentTrTextarea) {
        console.error('Content textareas not found');
        return;
    }

    // Tab switching functionality
    const tabEn = document.getElementById('tab-en');
    const tabTr = document.getElementById('tab-tr');
    const panelEn = document.getElementById('panel-en');
    const panelTr = document.getElementById('panel-tr');

    function switchTab(lang) {
        if (lang === 'en') {
            tabEn.classList.add('bg-blue-600', 'text-white');
            tabEn.classList.remove('bg-gray-200', 'text-gray-700');
            tabTr.classList.remove('bg-blue-600', 'text-white');
            tabTr.classList.add('bg-gray-200', 'text-gray-700');
            panelEn.classList.remove('hidden');
            panelTr.classList.add('hidden');
            tabEn.setAttribute('aria-selected', 'true');
            tabTr.setAttribute('aria-selected', 'false');
        } else {
            tabTr.classList.add('bg-blue-600', 'text-white');
            tabTr.classList.remove('bg-gray-200', 'text-gray-700');
            tabEn.classList.remove('bg-blue-600', 'text-white');
            tabEn.classList.add('bg-gray-200', 'text-gray-700');
            panelTr.classList.remove('hidden');
            panelEn.classList.add('hidden');
            tabTr.setAttribute('aria-selected', 'true');
            tabEn.setAttribute('aria-selected', 'false');
        }
    }

    tabEn.addEventListener('click', () => switchTab('en'));
    tabTr.addEventListener('click', () => switchTab('tr'));

    // Create toolbar buttons
    function createToolbar(toolbarId, editor) {
        const toolbar = document.getElementById(toolbarId);
        
        const buttons = [
            { name: 'Bold', icon: 'B', command: () => editor.chain().focus().toggleBold().run(), shortcut: 'Ctrl+B', level: null },
            { name: 'Italic', icon: 'I', command: () => editor.chain().focus().toggleItalic().run(), shortcut: 'Ctrl+I', level: null },
            { name: 'Code', icon: '</>', command: () => editor.chain().focus().toggleCode().run(), shortcut: 'Ctrl+E', level: null },
            { name: 'H1', icon: 'H1', command: () => editor.chain().focus().toggleHeading({ level: 1 }).run(), shortcut: 'Ctrl+Shift+1', level: 1 },
            { name: 'H2', icon: 'H2', command: () => editor.chain().focus().toggleHeading({ level: 2 }).run(), shortcut: 'Ctrl+Shift+2', level: 2 },
            { name: 'H3', icon: 'H3', command: () => editor.chain().focus().toggleHeading({ level: 3 }).run(), shortcut: 'Ctrl+Shift+3', level: 3 },
            { name: 'H4', icon: 'H4', command: () => editor.chain().focus().toggleHeading({ level: 4 }).run(), shortcut: 'Ctrl+Shift+4', level: 4 },
            { name: 'Bullet List', icon: '• List', command: () => editor.chain().focus().toggleBulletList().run(), shortcut: 'Ctrl+Shift+8', level: null },
            { name: 'Ordered List', icon: '1. List', command: () => editor.chain().focus().toggleOrderedList().run(), shortcut: 'Ctrl+Shift+7', level: null },
            { name: 'Code Block', icon: '{ }', command: () => editor.chain().focus().toggleCodeBlock().run(), shortcut: 'Ctrl+Shift+C', level: null },
            { name: 'Blockquote', icon: '" "', command: () => editor.chain().focus().toggleBlockquote().run(), shortcut: 'Ctrl+Shift+B', level: null },
            { name: 'Horizontal Rule', icon: '—', command: () => editor.chain().focus().setHorizontalRule().run(), shortcut: null, level: null },
        ];

        buttons.forEach(btn => {
            const button = document.createElement('button');
            button.type = 'button';
            button.innerHTML = btn.icon;
            button.title = btn.name + (btn.shortcut ? ` (${btn.shortcut})` : '');
            button.setAttribute('aria-label', btn.title);
            
            button.addEventListener('click', (e) => {
                e.preventDefault();
                btn.command();
                updateActiveStates();
            });

            toolbar.appendChild(button);
        });

        function updateActiveStates() {
            const buttons = toolbar.querySelectorAll('button');
            buttons[0].classList.toggle('is-active', editor.isActive('bold'));
            buttons[1].classList.toggle('is-active', editor.isActive('italic'));
            buttons[2].classList.toggle('is-active', editor.isActive('code'));
            buttons[3].classList.toggle('is-active', editor.isActive('heading', { level: 1 }));
            buttons[4].classList.toggle('is-active', editor.isActive('heading', { level: 2 }));
            buttons[5].classList.toggle('is-active', editor.isActive('heading', { level: 3 }));
            buttons[6].classList.toggle('is-active', editor.isActive('heading', { level: 4 }));
            buttons[7].classList.toggle('is-active', editor.isActive('bulletList'));
            buttons[8].classList.toggle('is-active', editor.isActive('orderedList'));
            buttons[9].classList.toggle('is-active', editor.isActive('codeBlock'));
            buttons[10].classList.toggle('is-active', editor.isActive('blockquote'));
        }

        editor.on('selectionUpdate', updateActiveStates);
        editor.on('transaction', updateActiveStates);
    }

    // Initialize English Editor
    const editorEn = new Editor({
        element: document.querySelector('#editor-en'),
        extensions: [StarterKit],
        content: contentEnTextarea.value || '',
        onUpdate: ({ editor }) => {
            contentEnTextarea.value = editor.getHTML();
        },
        editorProps: {
            attributes: {
                'aria-label': 'English content editor',
                'role': 'textbox',
                'aria-multiline': 'true'
            }
        }
    });

    createToolbar('toolbar-en', editorEn);

    // Initialize Turkish Editor
    const editorTr = new Editor({
        element: document.querySelector('#editor-tr'),
        extensions: [StarterKit],
        content: contentTrTextarea.value || '',
        onUpdate: ({ editor }) => {
            contentTrTextarea.value = editor.getHTML();
        },
        editorProps: {
            attributes: {
                'aria-label': 'Turkish content editor',
                'role': 'textbox',
                'aria-multiline': 'true'
            }
        }
    });

    createToolbar('toolbar-tr', editorTr);

    // Auto-generate slug from English title
    const titleEnInput = document.getElementById('id_title_en');
    const slugInput = document.getElementById('id_slug');
    
    if (titleEnInput && slugInput && !slugInput.value) {
        titleEnInput.addEventListener('input', function() {
            const slug = this.value
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '');
            slugInput.value = slug;
        });
    }

    // Ensure textareas are updated before form submission
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            contentEnTextarea.value = editorEn.getHTML();
            contentTrTextarea.value = editorTr.getHTML();
        });
    }

    console.log('TipTap editors initialized successfully');
});
