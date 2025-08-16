// Narrative Viewer JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Bootstrap tabs
    const triggerTabList = document.querySelectorAll('#narrativeTabs button[data-bs-toggle="tab"]');
    triggerTabList.forEach(triggerEl => {
        const tabTrigger = new bootstrap.Tab(triggerEl);
        
        triggerEl.addEventListener('click', event => {
            event.preventDefault();
            tabTrigger.show();
            
            // Add loading animation to tab content
            const targetId = triggerEl.getAttribute('data-bs-target');
            const targetPane = document.querySelector(targetId);
            
            if (targetPane) {
                targetPane.classList.add('loading');
                setTimeout(() => {
                    targetPane.classList.remove('loading');
                    targetPane.classList.add('loaded');
                }, 100);
            }
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll effects to navbar
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(52, 58, 64, 0.98)';
            navbar.style.backdropFilter = 'blur(15px)';
        } else {
            navbar.style.background = 'rgba(52, 58, 64, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.narrative-section, .skill-category, .outcome-card, .enhancement-item').forEach(el => {
        observer.observe(el);
    });

    // Add hover effects to enhancement items
    document.querySelectorAll('.enhancement-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click effects to skill categories
    document.querySelectorAll('.skill-category').forEach(category => {
        category.addEventListener('click', function() {
            // Add a subtle click effect
            this.style.transform = 'translateY(-3px) scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 150);
        });
    });

    // Add keyboard navigation for tabs
    document.addEventListener('keydown', function(e) {
        const activeTab = document.querySelector('#narrativeTabs .nav-link.active');
        const tabList = Array.from(document.querySelectorAll('#narrativeTabs .nav-link'));
        const currentIndex = tabList.indexOf(activeTab);
        
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = (currentIndex + 1) % tabList.length;
            tabList[nextIndex].click();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = currentIndex === 0 ? tabList.length - 1 : currentIndex - 1;
            tabList[prevIndex].click();
        }
    });

    // Add progress indicator for narrative sections
    function updateProgress() {
        const sections = document.querySelectorAll('.narrative-section');
        const totalSections = sections.length;
        let visibleSections = 0;
        
        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                visibleSections++;
            }
        });
        
        const progress = (visibleSections / totalSections) * 100;
        
        // Update progress bar if it exists
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }

    // Throttle scroll events for performance
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateProgress);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick);

    // Add print functionality
    const printButton = document.createElement('button');
    printButton.innerHTML = '<i class="fas fa-print me-2"></i>Print Narrative';
    printButton.className = 'btn btn-outline-primary position-fixed';
    printButton.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 25px; padding: 0.75rem 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);';
    
    printButton.addEventListener('click', function() {
        window.print();
    });
    
    document.body.appendChild(printButton);

    // Add table of contents functionality
    function createTableOfContents() {
        const sections = document.querySelectorAll('.narrative-section h4');
        const tocContainer = document.createElement('div');
        tocContainer.className = 'table-of-contents';
        tocContainer.innerHTML = '<h5><i class="fas fa-list me-2"></i>Table of Contents</h5><ul></ul>';
        
        const tocList = tocContainer.querySelector('ul');
        
        sections.forEach((section, index) => {
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            link.textContent = section.textContent.replace(/[^\w\s]/gi, '').trim();
            link.href = `#section-${index}`;
            link.className = 'toc-link';
            
            section.id = `section-${index}`;
            
            listItem.appendChild(link);
            tocList.appendChild(listItem);
        });
        
        // Insert TOC after the first paragraph
        const firstSection = document.querySelector('.narrative-section');
        if (firstSection) {
            firstSection.parentNode.insertBefore(tocContainer, firstSection);
        }
    }

    // Initialize table of contents
    createTableOfContents();

    // Add smooth scrolling for TOC links
    document.querySelectorAll('.toc-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 100;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add search functionality
    function addSearchFunctionality() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container mb-4';
        searchContainer.innerHTML = `
            <div class="input-group">
                <span class="input-group-text"><i class="fas fa-search"></i></span>
                <input type="text" class="form-control" id="narrativeSearch" placeholder="Search narrative content...">
                <button class="btn btn-outline-secondary" type="button" id="clearSearch">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        const narrativeContent = document.querySelector('.narrative-content .container');
        if (narrativeContent) {
            narrativeContent.insertBefore(searchContainer, narrativeContent.firstChild);
        }
        
        const searchInput = document.getElementById('narrativeSearch');
        const clearButton = document.getElementById('clearSearch');
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const sections = document.querySelectorAll('.narrative-section');
            
            sections.forEach(section => {
                const text = section.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    section.style.display = 'block';
                    section.style.opacity = '1';
                } else {
                    section.style.display = 'none';
                    section.style.opacity = '0.3';
                }
            });
        });
        
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            document.querySelectorAll('.narrative-section').forEach(section => {
                section.style.display = 'block';
                section.style.opacity = '1';
            });
        });
    }

    // Initialize search functionality
    addSearchFunctionality();

    // Add loading animation for tab content
    function addLoadingAnimation() {
        const tabPanes = document.querySelectorAll('.tab-pane');
        tabPanes.forEach(pane => {
            pane.classList.add('loading');
            setTimeout(() => {
                pane.classList.remove('loading');
                pane.classList.add('loaded');
            }, 300);
        });
    }

    // Initialize loading animation
    addLoadingAnimation();

    // Add accessibility features
    function addAccessibilityFeatures() {
        // Add ARIA labels
        document.querySelectorAll('.nav-link').forEach(link => {
            link.setAttribute('aria-label', link.textContent.trim());
        });
        
        // Add skip to content link
        const skipLink = document.createElement('a');
        skipLink.href = '#narrative-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.style.cssText = 'position: absolute; top: -40px; left: 6px; background: #000; color: white; padding: 8px; text-decoration: none; z-index: 10000;';
        
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Add focus styles
        document.querySelectorAll('button, a, input').forEach(element => {
            element.addEventListener('focus', function() {
                this.style.outline = '2px solid var(--primary-color)';
                this.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', function() {
                this.style.outline = 'none';
            });
        });
    }

    // Initialize accessibility features
    addAccessibilityFeatures();

    // Add performance monitoring
    function addPerformanceMonitoring() {
        // Monitor tab switching performance
        let tabSwitchStart;
        
        document.querySelectorAll('#narrativeTabs button').forEach(button => {
            button.addEventListener('click', function() {
                tabSwitchStart = performance.now();
            });
        });
        
        // Monitor when tab content is loaded
        document.querySelectorAll('.tab-pane').forEach(pane => {
            const observer = new MutationObserver(function(mutations) {
                if (tabSwitchStart) {
                    const tabSwitchTime = performance.now() - tabSwitchStart;
                    console.log(`Tab switch completed in ${tabSwitchTime.toFixed(2)}ms`);
                    tabSwitchStart = null;
                }
            });
            
            observer.observe(pane, { childList: true, subtree: true });
        });
    }

    // Initialize performance monitoring
    addPerformanceMonitoring();

    console.log('Narrative viewer initialized successfully!');
});
