// FAQ Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const faqToggles = document.querySelectorAll('.faq-toggle');
    
    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const faqItem = this.closest('.faq-item');
            const answer = faqItem.querySelector('.faq-answer');
            const isActive = answer && !answer.classList.contains('hidden');
            
            // Close all other FAQs
            faqToggles.forEach(otherToggle => {
                if (otherToggle !== this) {
                    const otherFaqItem = otherToggle.closest('.faq-item');
                    const otherAnswer = otherFaqItem.querySelector('.faq-answer');
                    if (otherAnswer) {
                        otherAnswer.classList.add('hidden');
                    }
                }
            });
            
            // Toggle current FAQ
            if (answer) {
                if (isActive) {
                    answer.classList.add('hidden');
                } else {
                    answer.classList.remove('hidden');
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

