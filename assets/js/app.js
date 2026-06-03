/* 
    Saka-NLP Global Scripts 📜
    Handles: Theme Toggle, Copy to Clipboard, and Scroll Spy.
*/

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initCopyButtons();
    initScrollSpy();
});

/**
 * Theme Management (Light/Dark)
 */
function initTheme() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;

    const rootElt = document.documentElement;

    const applyTheme = (theme) => {
        if (theme === 'light') {
            rootElt.setAttribute('data-theme', 'light');
        } else {
            rootElt.removeAttribute('data-theme');
        }
    };

    const savedTheme = localStorage.getItem('theme');
    const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    const initTheme = savedTheme || (systemPrefersLight ? 'light' : 'dark');

    applyTheme(initTheme);

    themeToggleBtn.addEventListener('click', () => {
        const isLight = rootElt.getAttribute('data-theme') === 'light';
        const newTheme = isLight ? 'dark' : 'light';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

/**
 * Copy to Clipboard Functionality
 */
function initCopyButtons() {
    // We attach the copy function to the window so the inline onclick works, 
    // but better practice is event delegation or querySelector.
    window.copyCode = function (btn) {
        const code = btn.parentElement.nextElementSibling.innerText;
        navigator.clipboard.writeText(code).then(() => {
            const originalText = btn.innerText;
            btn.innerText = "Tersalin!";
            btn.style.borderColor = "var(--accent)";
            btn.style.color = "var(--accent)";
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.borderColor = "var(--border)";
                btn.style.color = "var(--text-dim)";
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    };
}

/**
 * Scroll Spy for Documentation Navigation
 */
function initScrollSpy() {
    const sections = document.querySelectorAll('.docs-section, .page-header');
    const navLinks = document.querySelectorAll('.nav-link');
    if (sections.length === 0 || navLinks.length === 0) return;

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    });
}
