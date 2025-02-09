document.addEventListener('DOMContentLoaded', function () {
    AOS.init();

    function initVanta() {
        // Check if a VANTA effect is already initialized and destroy it
        if (window.vantaEffect) {
            window.vantaEffect.destroy(); 
        }

        var fullPage = document.body; // Target the entire body or a full-screen container

        // Ensure dimensions are accurate before initializing VANTA
        var width = window.innerWidth;
        var height = window.innerHeight;

        // Initialize VANTA Globe effect for larger screens
        if (window.innerWidth > 576) {
            fullPage.style.backgroundColor = 'transparent';

            // Use requestAnimationFrame for smooth initialization
            window.requestAnimationFrame(function() {
                window.vantaEffect = VANTA.GLOBE({
                    el: fullPage, // Target the entire page or any other container
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: height,
                    minWidth: width,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x2b7a78, // Set the color for the globe effect
                    size: 1.40, // Set the size of the globe
                    backgroundColor: 0xdef2f1 // Set the background color for the effect
                });
            });
        } else {
            // For smaller screens, set a default background color
            fullPage.style.backgroundColor = '#243282';
            if (window.vantaEffect) {
                window.vantaEffect.destroy(); // Destroy any active effect on smaller screens
            }
        }
    }

    initVanta(); // Initialize the VANTA effect

    // Reinitialize the VANTA effect on resize to ensure it's responsive
    window.addEventListener('resize', function() {
        initVanta();
    });

    // Ensure initialization when the window is fully loaded
    window.addEventListener('load', function() {
        initVanta();
    });
});
