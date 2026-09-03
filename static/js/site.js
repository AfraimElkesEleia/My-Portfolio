(() => {
    const root = document.documentElement;
    const progress = document.querySelector('.scroll-progress span');
    const glow = document.querySelector('.cursor-glow');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const updateProgress = () => {
        const scrollable = root.scrollHeight - window.innerHeight;
        const value = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
        if (progress) progress.style.width = `${value}%`;
    };

    let progressQueued = false;
    window.addEventListener('scroll', () => {
        if (progressQueued) return;
        progressQueued = true;
        requestAnimationFrame(() => {
            updateProgress();
            progressQueued = false;
        });
    }, { passive: true });
    updateProgress();

    const reveals = document.querySelectorAll('.reveal');
    if (reduceMotion || !('IntersectionObserver' in window)) {
        reveals.forEach((item) => item.classList.add('is-visible'));
    } else {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.16, rootMargin: '0px 0px -5% 0px' });
        reveals.forEach((item) => revealObserver.observe(item));
    }

    const navLinks = [...document.querySelectorAll('nav a[href^="#"]')];
    const sections = navLinks.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
    if ('IntersectionObserver' in window) {
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                navLinks.forEach((link) => {
                    link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
                });
            });
        }, { rootMargin: '-35% 0px -55% 0px' });
        sections.forEach((section) => sectionObserver.observe(section));
    }

    if (!reduceMotion && window.matchMedia('(pointer: fine)').matches) {
        window.addEventListener('pointermove', (event) => {
            if (!glow) return;
            glow.style.left = `${event.clientX}px`;
            glow.style.top = `${event.clientY}px`;
        }, { passive: true });

        document.querySelectorAll('[data-tilt]').forEach((item) => {
            const target = item.querySelector('.portrait-card') || item.querySelector('.project-visual');
            if (!target) return;
            item.addEventListener('pointermove', (event) => {
                const bounds = item.getBoundingClientRect();
                const x = (event.clientX - bounds.left) / bounds.width - .5;
                const y = (event.clientY - bounds.top) / bounds.height - .5;
                target.style.transform = `perspective(1000px) rotateX(${-y * 2.5}deg) rotateY(${x * 2.5}deg)`;
            });
            item.addEventListener('pointerleave', () => { target.style.transform = ''; });
        });

        document.querySelectorAll('.magnetic').forEach((item) => {
            item.addEventListener('pointermove', (event) => {
                const bounds = item.getBoundingClientRect();
                const x = (event.clientX - bounds.left - bounds.width / 2) * .14;
                const y = (event.clientY - bounds.top - bounds.height / 2) * .14;
                item.style.transform = `translate(${x}px, ${y}px)`;
            });
            item.addEventListener('pointerleave', () => { item.style.transform = ''; });
        });
    }
})();
