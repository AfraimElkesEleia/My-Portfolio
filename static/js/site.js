(() => {
    const root = document.documentElement;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const scheduleFrame = (callback) => {
        let frameId = null;
        let latestArguments = [];

        return (...args) => {
            latestArguments = args;
            if (frameId !== null) return;

            frameId = requestAnimationFrame(() => {
                frameId = null;
                callback(...latestArguments);
            });
        };
    };

    const initScrollProgress = () => {
        const progress = document.querySelector('.scroll-progress span');
        if (!progress) return;

        const update = () => {
            const scrollable = root.scrollHeight - window.innerHeight;
            const percentage = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
            progress.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
        };
        const scheduleUpdate = scheduleFrame(update);

        window.addEventListener('scroll', scheduleUpdate, { passive: true });
        window.addEventListener('resize', scheduleUpdate, { passive: true });
        update();
    };

    const setRevealDelays = () => {
        document.querySelectorAll('.section, .contact-section').forEach((group) => {
            group.querySelectorAll('.reveal').forEach((item, index) => {
                item.style.setProperty('--reveal-delay', `${Math.min(index * 85, 340)}ms`);
            });
        });
    };

    const finishReveal = (item) => {
        item.classList.add('is-visible', 'reveal-complete');
    };

    const initRevealAnimations = () => {
        setRevealDelays();
        const reveals = document.querySelectorAll('.reveal');

        if (reduceMotion || !('IntersectionObserver' in window)) {
            reveals.forEach(finishReveal);
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                requestAnimationFrame(() => entry.target.classList.add('is-visible'));
                observer.unobserve(entry.target);
            });
        }, {
            threshold: window.innerWidth <= 680 ? 0.08 : 0.14,
            rootMargin: '0px 0px -10% 0px',
        });

        reveals.forEach((item) => {
            const releasePerformanceHint = (event) => {
                if (event.target !== item || event.propertyName !== 'transform') return;
                item.classList.add('reveal-complete');
                item.removeEventListener('transitionend', releasePerformanceHint);
            };

            item.addEventListener('transitionend', releasePerformanceHint);
            observer.observe(item);
        });
    };

    const initActiveNavigation = () => {
        if (!('IntersectionObserver' in window)) return;

        const links = [...document.querySelectorAll('nav a[href^="#"]')];
        const sections = links
            .map((link) => document.querySelector(link.getAttribute('href')))
            .filter(Boolean);
        if (!links.length || !sections.length) return;

        const observer = new IntersectionObserver((entries) => {
            const activeEntry = entries.find((entry) => entry.isIntersecting);
            if (!activeEntry) return;

            links.forEach((link) => {
                link.classList.toggle(
                    'active',
                    link.getAttribute('href') === `#${activeEntry.target.id}`,
                );
            });
        }, { rootMargin: '-35% 0px -55% 0px' });

        sections.forEach((section) => observer.observe(section));
    };

    const initCursorGlow = () => {
        const glow = document.querySelector('.cursor-glow');
        if (!glow) return;

        const updatePosition = scheduleFrame((x, y) => {
            glow.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        });
        window.addEventListener('pointermove', (event) => {
            updatePosition(event.clientX, event.clientY);
        }, { passive: true });
    };

    const initTiltEffects = () => {
        document.querySelectorAll('[data-tilt]').forEach((item) => {
            const target = item.querySelector('.portrait-card, .project-visual');
            if (!target) return;

            const updateTilt = scheduleFrame((clientX, clientY) => {
                const bounds = item.getBoundingClientRect();
                const x = (clientX - bounds.left) / bounds.width - 0.5;
                const y = (clientY - bounds.top) / bounds.height - 0.5;
                target.style.transform = `perspective(1000px) rotateX(${-y * 2.5}deg) rotateY(${x * 2.5}deg)`;
            });

            item.addEventListener('pointermove', (event) => {
                updateTilt(event.clientX, event.clientY);
            }, { passive: true });
            item.addEventListener('pointerleave', () => {
                target.style.transform = '';
            });
        });
    };

    const initMagneticButtons = () => {
        document.querySelectorAll('.magnetic').forEach((item) => {
            const updatePosition = scheduleFrame((clientX, clientY) => {
                const bounds = item.getBoundingClientRect();
                const x = (clientX - bounds.left - bounds.width / 2) * 0.14;
                const y = (clientY - bounds.top - bounds.height / 2) * 0.14;
                item.style.transform = `translate3d(${x}px, ${y}px, 0)`;
            });

            item.addEventListener('pointermove', (event) => {
                updatePosition(event.clientX, event.clientY);
            }, { passive: true });
            item.addEventListener('pointerleave', () => {
                item.style.transform = '';
            });
        });
    };

    const initPointerEffects = () => {
        if (reduceMotion || !window.matchMedia('(pointer: fine)').matches) return;
        initCursorGlow();
        initTiltEffects();
        initMagneticButtons();
    };

    initScrollProgress();
    initRevealAnimations();
    initActiveNavigation();
    initPointerEffects();
})();
