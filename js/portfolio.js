// Geometric network background behind hero sections
(function () {
  function createNetworkForHero(heroEl) {
    const canvas = document.createElement('canvas');
    canvas.className = 'network-canvas';
    heroEl.appendChild(canvas);
    const ctx = canvas.getContext('2d');

    let width = 0, height = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
    let points = [], animationId = 0;

    function resize() {
      width = heroEl.clientWidth;
      height = heroEl.clientHeight;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      initPoints();
    }

    function initPoints() {
      const area = width * height;
      const density = 0.00014; // slightly denser
      const count = Math.max(30, Math.min(180, Math.floor(area * density)));
      points = new Array(count).fill(0).map(() => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35
      }));
    }

    function step() {
      ctx.clearRect(0, 0, width, height);
      // Move points
      for (let p of points) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;
      }
      // Draw connections (thin, dotted look via alpha modulation)
      const maxDist = Math.min(width, height) * 0.22;
      for (let i = 0; i < points.length; i++) {
        for (let j = i + 1; j < points.length; j++) {
          const dx = points[i].x - points[j].x;
          const dy = points[i].y - points[j].y;
          const dist = Math.hypot(dx, dy);
          if (dist < maxDist) {
            const t = 1 - dist / maxDist;
            ctx.strokeStyle = `rgba(83,155,245,${0.30 * t})`;
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(points[i].x, points[i].y);
            ctx.lineTo(points[j].x, points[j].y);
            ctx.stroke();
          }
        }
      }
      // Draw nodes
      for (let p of points) {
        ctx.fillStyle = 'rgba(191,224,255,0.9)';
        ctx.beginPath();
        ctx.arc(p.x, p.y, 1.2, 0, Math.PI * 2);
        ctx.fill();
      }
      animationId = requestAnimationFrame(step);
    }

    const ro = new ResizeObserver(resize);
    ro.observe(heroEl);
    resize();
    step();

    // Cleanup on page hide/navigation (best effort)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) cancelAnimationFrame(animationId); else step();
    });
  }

  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.hero').forEach(hero => {
      // Avoid duplicating if already present
      if (!hero.querySelector('canvas.network-canvas')) {
        createNetworkForHero(hero);
      }
    });
  });
})();
// Portfolio JavaScript - Interactive Features and Animations

document.addEventListener('DOMContentLoaded', function() {
    // Navigation mobile: ouverture/fermeture
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // Défilement fluide avec compensation de la barre de navigation
    const navbar = document.querySelector('.navbar');
    const navbarOffset = navbar ? (navbar.offsetHeight || 80) : 80;
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            const target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            const targetTop = Math.max(0, target.getBoundingClientRect().top + window.pageYOffset - navbarOffset);
            window.scrollTo({ top: targetTop, behavior: 'smooth' });
        });
    });

    // Style de la barre de navigation au scroll
    if (navbar) {
        const applyNavbarStyle = () => {
            if (window.scrollY > 100) {
                navbar.style.background = 'rgba(34, 39, 46, 0.95)';
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.25)';
            } else {
                navbar.style.background = 'rgba(34, 39, 46, 0.85)';
                navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.2)';
            }
        };
        applyNavbarStyle();
        window.addEventListener('scroll', applyNavbarStyle);
    }

    // Mise en évidence du lien actif
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    const highlightActiveLink = () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - (navbarOffset + 20);
            const sectionBottom = sectionTop + section.clientHeight;
            if (window.scrollY >= sectionTop && window.scrollY < sectionBottom) {
                current = section.getAttribute('id') || '';
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href') || '';
            if (href === `#${current}`) link.classList.add('active');
        });
    };
    window.addEventListener('scroll', highlightActiveLink);
    highlightActiveLink();

    // Animation d'apparition au scroll
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    document.querySelectorAll('.section-title, .about-content, .skill-category, .project-card, .stat').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(el);
    });

    // Animation des barres de compétences (accepte 75, "75", "75%")
    const normalizePercent = (val) => {
        if (val == null) return 0;
        const num = parseFloat(String(val).toString().replace(/[^0-9.]/g, ''));
        if (isNaN(num)) return 0;
        return Math.max(0, Math.min(100, num));
    };
    const skillBars = document.querySelectorAll('.skill-progress');
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const data = bar.getAttribute('data-width');
                const percent = normalizePercent(data);
                bar.style.width = percent + '%';
                skillObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    skillBars.forEach(bar => skillObserver.observe(bar));

    // Filtrage des projets
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                const show = filter === 'all' || category === filter;
                card.style.display = show ? 'block' : 'none';
                if (show) card.style.animation = 'fadeInUp 0.6s ease';
            });
        });
    });

    // Compteurs des stats (gère valeurs avec +)
    const stats = document.querySelectorAll('.stat h3');
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const raw = (el.textContent || '').replace(/[^0-9]/g, '');
            const finalValue = parseInt(raw || '0', 10);
            let currentValue = 0;
            const steps = 50;
            const increment = Math.max(1, Math.round(finalValue / steps));
            const interval = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    el.textContent = finalValue + '+';
                    clearInterval(interval);
                } else {
                    el.textContent = currentValue + '+';
                }
            }, 30);
            statsObserver.unobserve(el);
        });
    }, { threshold: 0.5 });
    stats.forEach(s => statsObserver.observe(s));

    // Formulaire de contact (envoi via mailto)
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const nameInput = this.querySelector('input[name="name"], input[placeholder="Your Name"], input[type="text"]');
            const emailInput = this.querySelector('input[name="email"], input[type="email"]');
            const subjectInput = this.querySelector('input[name="subject"], input[placeholder="Subject"]');
            const messageInput = this.querySelector('textarea[name="message"], textarea');
            const name = nameInput ? nameInput.value.trim() : '';
            const email = emailInput ? emailInput.value.trim() : '';
            const subject = subjectInput ? subjectInput.value.trim() : '';
            const message = messageInput ? messageInput.value.trim() : '';
            const isFormSubmitService = (this.getAttribute('action') || '').includes('formsubmit.co');
            if (!name || !email || !subject || !message) {
                e.preventDefault();
                alert('Veuillez remplir tous les champs requis.');
                return;
            }
            if (isFormSubmitService) {
                // Laisser l'envoi natif au service FormSubmit
                return;
            }
            // Fallback: mailto si aucun service n'est configuré
            e.preventDefault();
            const to = 'sighanobob@yahoo.fr';
            const mailSubject = subject;
            const mailBody = `Nom: ${name}\nEmail: ${email}\n\n${message}`;
            const mailtoLink = `mailto:${to}?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(mailBody)}`;
            window.location.href = mailtoLink;
        });
    }

    // Indicateur de scroll: vers #about ou #apropos selon disponibilité
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            const target = document.querySelector('#about') || document.querySelector('#apropos');
            if (!target) return;
            const targetTop = Math.max(0, target.getBoundingClientRect().top + window.pageYOffset - navbarOffset);
            window.scrollTo({ top: targetTop, behavior: 'smooth' });
        });
    }

    // Effet parallaxe de l'image héros
    const heroImage = document.querySelector('.hero-image');
    const onParallax = () => {
        const scrolled = window.pageYOffset;
        if (heroImage && scrolled < window.innerHeight) {
            heroImage.style.transform = 'translateY(' + (scrolled * 0.3) + 'px)';
        }
    };
    window.addEventListener('scroll', onParallax);
    onParallax();

    // Effets hover cartes projets
    const projectCardsForHover = document.querySelectorAll('.project-card');
    projectCardsForHover.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Liens sociaux hover
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) rotate(10deg)';
        });
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotate(0deg)';
        });
    });

    // Animation fade-in au chargement
    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease';
        requestAnimationFrame(() => {
            setTimeout(() => { document.body.style.opacity = '1'; }, 100);
        });
    });

    // Carrousel About - autoplay en boucle
    const aboutCarouselTrack = document.querySelector('.about-carousel .carousel-track');
    const aboutCarouselContainer = document.querySelector('.about-carousel');
    if (aboutCarouselTrack && aboutCarouselContainer) {
        let index = 0;
        const slides = aboutCarouselTrack.querySelectorAll('.carousel-slide');
        const total = slides.length;
        const goTo = (i) => {
            index = (i + total) % total;
            const offset = -index * aboutCarouselContainer.clientWidth;
            aboutCarouselTrack.style.transform = `translateX(${offset}px)`;
            aboutCarouselTrack.style.transition = 'transform 0.6s ease';
        };
        const onResize = () => { goTo(index); };
        window.addEventListener('resize', onResize);
        let timer = setInterval(() => { goTo(index + 1); }, 3000);
        // Pause au survol
        aboutCarouselContainer.addEventListener('mouseenter', () => { clearInterval(timer); });
        aboutCarouselContainer.addEventListener('mouseleave', () => { timer = setInterval(() => { goTo(index + 1); }, 3000); });
        // Contrôles manuels
        const prevBtn = aboutCarouselContainer.querySelector('.carousel-btn.prev');
        const nextBtn = aboutCarouselContainer.querySelector('.carousel-btn.next');
        if (prevBtn) prevBtn.addEventListener('click', () => { goTo(index - 1); });
        if (nextBtn) nextBtn.addEventListener('click', () => { goTo(index + 1); });
        goTo(0);
    }

    // Easter egg Konami
    let konamiCode = [];
    const konamiSequence = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','KeyB','KeyA'];
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.code);
        if (konamiCode.length > konamiSequence.length) konamiCode.shift();
        if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
            document.body.style.animation = 'rainbow 2s ease infinite';
            setTimeout(() => { document.body.style.animation = ''; }, 5000);
        }
    });
    const style = document.createElement('style');
    style.textContent = '@keyframes rainbow { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }';
    document.head.appendChild(style);
});

// Utilitaires
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => { clearTimeout(timeout); func(...args); };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handler de scroll optimisé (réservé pour futurs usages)
const optimizedScrollHandler = debounce(function() {
    // point d'extension
}, 10);
window.addEventListener('scroll', optimizedScrollHandler);