import os

target_file = r"D:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

old_landing_start = """# ---------------------------------------------------------
# 1. LANDING PAGE (STARLINK BACKGROUND)
# ---------------------------------------------------------
if not st.session_state.app_started:"""

old_landing_end = """# ---------------------------------------------------------
# 2. MAIN APPLICATION
# ---------------------------------------------------------"""

new_landing = """import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. LANDING PAGE (DENSE BRAIN STARLINK BACKGROUND)
# ---------------------------------------------------------
if not st.session_state.app_started:
    st.markdown('''
    <style>
    /* Hide default Streamlit elements */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stApp > header { display: none !important; }
    
    /* Make app full dark */
    .stApp {
        background-color: #020617 !important;
    }
    
    /* Remove default padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Start Button Styling that floats above the interactive iframe */
    .start-btn-container {
        position: absolute;
        top: 65vh;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        text-align: center;
    }
    div.stButton > button {
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        background: rgba(14, 165, 233, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #e0f2fe !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.2), inset 0 0 10px rgba(14, 165, 233, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div.stButton > button:hover {
        transform: scale(1.05) translateY(-2px) !important;
        background: rgba(14, 165, 233, 0.3) !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.5), inset 0 0 20px rgba(56, 189, 248, 0.3) !important;
        border-color: rgba(125, 211, 252, 0.8) !important;
        color: white !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    # Render a full-screen HTML component with Three.js/Particles for a dense brain network
    html_code = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; padding: 0; background-color: #020617; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
            #overlay { position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%); z-index: 10; text-align: center; pointer-events: none; width: 100%; }
            .title { font-size: 5rem; font-weight: 800; background: linear-gradient(135deg, #7dd3fc, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; text-shadow: 0 0 30px rgba(56,189,248,0.2); animation: pulse 4s infinite alternate; }
            .subtitle { font-size: 1.25rem; color: #94a3b8; margin-top: 1rem; font-weight: 300; letter-spacing: 1px; }
            @keyframes pulse { 0% { filter: brightness(1) drop-shadow(0 0 10px rgba(56,189,248,0.1)); } 100% { filter: brightness(1.2) drop-shadow(0 0 25px rgba(56,189,248,0.4)); } }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="overlay">
            <h1 class="title">EverTutor</h1>
            <p class="subtitle">Your Personal AI Tutor</p>
        </div>
        <div id="canvas-container"></div>
        <script>
            // Initialize Three.js scene
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2('#020617', 0.001);
            
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 3000);
            camera.position.z = 800;

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor('#020617', 1);
            document.getElementById('canvas-container').appendChild(renderer.domElement);

            // Create Brain/Node Network points
            const particleCount = 2000;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const sizes = new Float32Array(particleCount);
            
            // Helper to create rough brain-like double hemisphere shape
            for(let i = 0; i < particleCount; i++) {
                // Spherical coordinates with some brain-like shaping logic
                let theta = Math.random() * Math.PI * 2;
                let phi = Math.acos((Math.random() * 2) - 1);
                
                // Base radius
                let r = 250 + Math.random() * 150;
                
                // Pinch the middle to make two hemispheres
                if (Math.abs(Math.sin(theta)) < 0.3) {
                    r *= 0.6 + (Math.abs(Math.sin(theta)) * 1.3);
                }
                // Flatten the bottom slightly
                if (Math.cos(phi) < -0.5) {
                    r *= 0.8;
                }

                let x = r * Math.sin(phi) * Math.cos(theta);
                let y = r * Math.cos(phi);
                let z = r * Math.sin(phi) * Math.sin(theta);
                
                // Add some noise
                x += (Math.random() - 0.5) * 40;
                y += (Math.random() - 0.5) * 40;
                z += (Math.random() - 0.5) * 40;

                positions[i*3] = x;
                positions[i*3+1] = y;
                positions[i*3+2] = z;
                
                sizes[i] = Math.random() * 2 + 1;
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            // Custom shader material for glowing nodes
            const material = new THREE.PointsMaterial({
                color: 0x38bdf8,
                size: 2.5,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            });

            const particles = new THREE.Points(geometry, material);
            scene.add(particles);

            // Connect lines between close nodes (Neural Connections)
            const lineMaterial = new THREE.LineBasicMaterial({
                color: 0x0ea5e9,
                transparent: true,
                opacity: 0.15,
                blending: THREE.AdditiveBlending
            });
            
            // Re-calculate lines dynamically is expensive, so we just build a static mesh of random lines 
            // that orbit together with the points.
            const lineGeo = new THREE.BufferGeometry();
            const linePos = [];
            const p = positions;
            let connections = 0;
            const maxConnectDist = 65;
            
            for(let i=0; i<particleCount; i++) {
                // limit connections per node for performance
                let nodeConnects = 0;
                for(let j=i+1; j<particleCount; j++) {
                    if(nodeConnects > 4) break;
                    
                    let dx = p[i*3] - p[j*3];
                    let dy = p[i*3+1] - p[j*3+1];
                    let dz = p[i*3+2] - p[j*3+2];
                    let dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
                    
                    if(dist < maxConnectDist) {
                        linePos.push(p[i*3], p[i*3+1], p[i*3+2]);
                        linePos.push(p[j*3], p[j*3+1], p[j*3+2]);
                        nodeConnects++;
                    }
                }
            }
            lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePos, 3));
            const lines = new THREE.LineSegments(lineGeo, lineMaterial);
            scene.add(lines);

            // Add subtle ambient blue light / glow in center
            const glowGeo = new THREE.SphereGeometry(200, 32, 32);
            const glowMat = new THREE.MeshBasicMaterial({
                color: 0x0369a1,
                transparent: true,
                opacity: 0.05,
                blending: THREE.AdditiveBlending
            });
            const glowMesh = new THREE.Mesh(glowGeo, glowMat);
            scene.add(glowMesh);

            // Mouse interaction
            let mouseX = 0;
            let mouseY = 0;
            document.addEventListener('mousemove', (event) => {
                mouseX = (event.clientX - window.innerWidth / 2) * 1.5;
                mouseY = (event.clientY - window.innerHeight / 2) * 1.5;
            });

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            // Animation Loop
            let time = 0;
            function animate() {
                requestAnimationFrame(animate);
                time += 0.002;
                
                // Slow rotation
                particles.rotation.y = time * 0.5;
                particles.rotation.z = time * 0.2;
                lines.rotation.y = time * 0.5;
                lines.rotation.z = time * 0.2;
                
                // Pulsing effect using scale
                let pulseBase = 1 + (Math.sin(time * 15) * 0.02);
                particles.scale.set(pulseBase, pulseBase, pulseBase);
                lines.scale.set(pulseBase, pulseBase, pulseBase);
                
                glowMesh.scale.set(pulseBase*1.2, pulseBase*1.2, pulseBase*1.2);

                // Mouse parallax
                camera.position.x += (mouseX - camera.position.x) * 0.05;
                camera.position.y += (-mouseY - camera.position.y) * 0.05;
                camera.lookAt(scene.position);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    '''
    
    # We place the HTML background taking the full viewport behind the button
    with st.container():
        components.html(html_code, height=1000, scrolling=False)
    
    # Place the start button centered
    st.markdown('<div class="start-btn-container">', unsafe_allow_html=True)
    if st.button("Initiate Link"):
        st.session_state.app_started = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. MAIN APPLICATION
# ---------------------------------------------------------"""

start_idx = content.find(old_landing_start)
end_idx = content.find(old_landing_end)

if start_idx != -1 and end_idx != -1:
    new_source = content[:start_idx] + new_landing + content[end_idx + len(old_landing_end):]
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(new_source)
    print("Successfully replaced landing page with Brain Network Starlink!")
else:
    print("Could not find insertion points, check logic.")
