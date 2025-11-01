// FAQ Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const faqToggles = document.querySelectorAll('.faq-toggle');
    
    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const faqItem = this.closest('.faq-item');
            const answer = faqItem.querySelector('.faq-answer');
            const isActive = this.classList.contains('active');
            
            // Close all other FAQs
            faqToggles.forEach(otherToggle => {
                if (otherToggle !== this) {
                    otherToggle.classList.remove('active');
                    const otherFaqItem = otherToggle.closest('.faq-item');
                    const otherAnswer = otherFaqItem.querySelector('.faq-answer');
                    if (otherAnswer) {
                        otherAnswer.classList.remove('show');
                        otherAnswer.classList.add('hidden');
                    }
                }
            });
            
            // Toggle current FAQ
            if (answer) {
                if (isActive) {
                    this.classList.remove('active');
                    answer.classList.remove('show');
                    answer.classList.add('hidden');
                } else {
                    this.classList.add('active');
                    answer.classList.remove('hidden');
                    answer.classList.add('show');
                }
            }
        });
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});