/* Background for each page */
document.addEventListener('DOMContentLoaded', function () {
    AOS.init();

    function initVanta() {
        if (window.vantaEffect) {
            window.vantaEffect.destroy(); 
        }
        
        /* Add background to full page */
        var fullPage = document.body; 

        /* Ensure accurate dimensions */
        var width = window.innerWidth;
        var height = window.innerHeight;

        /* Create globel effect */
        if (window.innerWidth > 576) {
            fullPage.style.backgroundColor = 'transparent';

            /* For smooth initialisation */
            window.requestAnimationFrame(function() {
                window.vantaEffect = VANTA.GLOBE({
                    el: fullPage, 
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: height,
                    minWidth: width,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x2b7a78, 
                    size: 1.40, 
                    backgroundColor: 0xdef2f1 
                });
            });
        } else {
            /* Smaller screens, set a default background colour */
            fullPage.style.backgroundColor = '#DEF2F1';
            if (window.vantaEffect) {
                window.vantaEffect.destroy(); 
            }
        }
    }

    /* Run background effect */
    initVanta(); 

    /* Reinitialise VANTA if page resizes for responsiveness */
    window.addEventListener('resize', function() {
        initVanta();
    });

    /* Initialise when window is fully loaded */
    window.addEventListener('load', function() {
        initVanta();
    });
});

/*  
Citation:
https://www.vantajs.com/?effect=globe#(backgroundAlpha:1,backgroundColor:#def2f1,color:#2b7a78,color2:16777215,gyroControls:!f,maxDistance:20,minHeight:200,minWidth:200,mouseControls:!t,points:10,scale:1,scaleMobile:1,showDots:!t,size:1.4000000000000001,spacing:15,touchControls:!t)

Found nice background here to use
*/
