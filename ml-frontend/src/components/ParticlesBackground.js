import React, { useEffect } from 'react';

const ParticlesBackground = () => {
  useEffect(() => {
    
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"; //Particles.js
    script.async = true;
    document.body.appendChild(script);

    
    script.onload = () => {
      if (window.particlesJS) {
        window.particlesJS('particles-js', {
          particles: {
            number: {
              value: 100,
              density: {
                enable: true,
                value_area: 800
              }
            },
            color: {
              value: '#00ffcc'
            },
            shape: {
              type: 'circle',
            },
            opacity: {
              value: 0.5,
              random: true,
              anim: {
                enable: true,
                speed: 1,
                opacity_min: 0.1
              }
            },
            size: {
              value: 3,
              random: true,
              anim: {
                enable: true,
                speed: 4,
                size_min: 0.1
              }
            },
            line_linked: {
              enable: true,
              distance: 150,
              color: '#00ffcc',
              opacity: 0.4,
              width: 1
            },
            move: {
              enable: true,
              speed: 1,
              direction: 'none',
              random: true,
              out_mode: 'out',
            }
          },
          interactivity: {
            events: {
              onhover: {
                enable: true,
                mode: 'repulse'
              }
            }
          }
        });
      }
    };

    
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return <div id="particles-js" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: -1, pointerEvents: 'none' }} />;
};

export default ParticlesBackground;

