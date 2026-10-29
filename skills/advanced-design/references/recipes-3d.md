# Recipes — Track A: Echtes 3D im Web (Three.js / WebGPU)

Enterprise-3D-Baukasten. Lokal gevendort (kein CDN): `three.module.js` + `three.core.js`
(z.B. unter `<static-root>/vendor/`). Importmap oder direkter relativer Import.

## 0. Szenen-Grundgerüst
```js
import * as THREE from './three.module.js';
const gl = new THREE.WebGLRenderer({ antialias:true, alpha:true, powerPreference:'high-performance',
  preserveDrawingBuffer:true });           // preserveDrawingBuffer: für Screenshots/Off-Screen
gl.setPixelRatio(Math.min(devicePixelRatio,2));
gl.outputColorSpace = THREE.SRGBColorSpace;
gl.toneMapping = THREE.ACESFilmicToneMapping;  // oder AgXToneMapping (neutraler, dann nachsättigen)
gl.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(40, w/h, 0.1, 100); cam.position.set(0,0,6);
```

## 1. IBL / Env-Map (größter Look-Hebel)
Eine gute Environment-Map lässt ALLE PBR-Materialien teuer aussehen. Prozedural (ohne HDRI-Datei):
```js
function makeEnv(renderer){
  const cv=document.createElement('canvas'); cv.width=512; cv.height=256; const g=cv.getContext('2d');
  const grad=g.createLinearGradient(0,0,0,256);
  grad.addColorStop(0,'#1b2128'); grad.addColorStop(.55,'#0c0f13'); grad.addColorStop(1,'#05070a');
  g.fillStyle=grad; g.fillRect(0,0,512,256);
  // Softbox-Streifen = gerichtete Glanzlichter auf Metall/Glas:
  g.fillStyle='rgba(190,208,222,.55)'; g.fillRect(56,36,130,26);
  g.fillStyle='rgba(95,155,176,.5)';   g.fillRect(320,58,120,20);
  const tex=new THREE.CanvasTexture(cv); tex.mapping=THREE.EquirectangularReflectionMapping;
  const p=new THREE.PMREMGenerator(renderer); const rt=p.fromEquirectangular(tex);
  tex.dispose(); p.dispose(); return rt.texture;
}
scene.environment = makeEnv(gl);   // MeshStandard/Physical nutzen das automatisch
```
Produktiv-Alternative: echtes `.hdr` via `RGBELoader` (Polyhaven, Lizenz prüfen). drei-Äquivalent: `<Environment preset="studio"/>`.

## 2. Glas (echt refraktiv) & Metall
```js
// GLAS: transmission braucht scene.environment (sonst tot)
const glas = new THREE.MeshPhysicalMaterial({ transmission:1.0, ior:1.45, thickness:0.6,
  roughness:0.05, clearcoat:1.0, clearcoatRoughness:0.05, envMapIntensity:1.4, transparent:true });
// METALL (unsere Slabs):
const metall = new THREE.MeshStandardMaterial({ color:0x2b2f36, metalness:1.0, roughness:0.22,
  envMapIntensity:1.3, emissive:new THREE.Color(0x5f9bb0), emissiveIntensity:0.05 });
```
drei-Spitze: `MeshTransmissionMaterial` (bessere Transmission mit Chromatic Aberration/Backside).

## 3. Licht (für den Fall ohne/mit wenig IBL)
```js
scene.add(new THREE.HemisphereLight(0xaebecd, 0x0a0c10, 1.0));
const key=new THREE.DirectionalLight(0xffffff,2.2); key.position.set(3,5,7); scene.add(key);
const rim=new THREE.PointLight(0x5f9bb0,40,26); rim.position.set(-4,2,3); scene.add(rim); // Akzent-Rim
```

## 4. Text AUF 3D-Objekten (unsere Diagramm-Slabs)
Text auf ein 2D-Canvas zeichnen → als `CanvasTexture` auf die Vorderseite kleben (dreht mit, bleibt „im" Objekt).
Front = `MeshBasicMaterial{map}` (unbeleuchtet → immer knackig lesbar), Seiten = Metall. Hoher DPR + `anisotropy`.
Alternative für massenhaft/scharfen Text: `troika-three-text` (SDF).

## 5. Kamera: Zoom, Blickwinkel, Fahrten
- **Zoom = Dolly (Position ändern), NICHT FOV.** FOV ändern verzerrt die Perspektive (nur bewusst für Vertigo/Hitchcock).
- **Weich & unterbrechbar:** `obj.pos.x = THREE.MathUtils.damp(obj.pos.x, target, 4, dt)` statt `lerp` — damp ist framerate-unabhängig.
- **Blickwinkel/Framing:** drei `CameraControls` (`.fitToBox(mesh)`, `.rotateTo`, `.dollyTo`), gedämpft.
- **Choreografierte Fahrten/Scroll-Flythrough:** `Theatre.js` (visueller Keyframe-Editor) — Kamera-Pfad an Scroll binden.
```js
let rx=0, ry=0;  // sanftes Maus-Parallax auf einer Group (begrenzt, Text lesbar)
onMouse = e => { const r=el.getBoundingClientRect();
  tx=((e.clientX-r.left)/r.width-.5)*0.5; ty=((e.clientY-r.top)/r.height-.5)*0.35; };
// im Loop: group.rotation.y = damp(group.rotation.y, tx, 5, dt); (analog x)
```

## 6. Post-Processing (der „teure" Film-Look)
Stack (EffectComposer bzw. `@react-three/postprocessing`): **Bloom** (nur echte Highlights glühen, threshold hoch)
→ **DepthOfField** (Hintergrund weich = Fokuslenkung) → **N8AO** (Kontakt-Schatten = Volumen).
Mobil deckeln/abschalten (teuer). Ohne R3F: `postprocessing` (pmndrs) Vanilla-API.

## 7. Isometrischer Tilt / Reveal (auch rein CSS auf dem Canvas-Container)
Für den „leicht schräg"-Look ohne volle 3D-Kamera: den Canvas/Container per CSS kippen
(`perspective` + `rotateX/rotateY`) — siehe `signature-elements.md §4` und `recipes-motion.md`.

## 8. Performance (Pflichtbasis)
- **Draw-Call-Budget < 100 auf Mobile.** `InstancedMesh`/`BatchedMesh`: 10k Objekte in 1 Draw-Call.
- `frameloop='demand'` (nur rendern wenn nötig) bzw. IntersectionObserver-Pause bei Off-Screen.
- Texturen als **KTX2/Basis** (GPU-komprimiert), Modelle glTF + Draco/Meshopt. LOD für Distanz.
- Post-Effekte sind die teuersten Posten → auf Zielgeräten messen, nicht auf dem Dev-Mac.

## 9. Zukunft (reif genug für Produktion, mit Fallback)
- **WebGPURenderer + TSL** (Three Shading Language): ein Shader-Graph → WGSL+GLSL, WebGL2-Fallback automatisch; Basis für GPU-Compute. Ab r171 produktionstauglich (stable später). Für Langzeit-Projekte planen.
- **GPU-Compute-Partikel** (TSL): 1M+ Partikel GPU-seitig für Hero-Effekte.
- **Gaussian Splatting** (three r186 `GaussianSplat` + Spark): fotorealistische gescannte Objekte als Viewer; Aufwand liegt im Capture→Cleanup.
> Unsicherheit: exakte Versions-/Support-Zahlen aus Sekundärquellen — vor Festlegung gegen offizielles Changelog/caniuse prüfen (siehe tech-matrix.md).
