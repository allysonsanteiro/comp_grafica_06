import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

function main() {
  const canvas = document.querySelector('#c');
  const renderer = new THREE.WebGLRenderer({canvas, antialias: true});
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();

  // --- Skybox com CubeTextureLoader ---
  const cubeLoader = new THREE.CubeTextureLoader();
  const skybox = cubeLoader.load([
    'cube_right.png', // direita
    'cube_left.png', // esquerda
    'cube_up.png', // cima
    'cube_down.png', // baixo
    'cube_back.png', // trás
    'cube_front.png', // frente

  ]);
  scene.background = skybox;

  // --- Câmera ---
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 3;

  // --- Controles Orbitais ---
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.update();

  // --- Cubo de teste ---
  const geometry = new THREE.BoxGeometry(1, 1, 1);
  const material = new THREE.MeshStandardMaterial({color: 0xff8844});
  const cube = new THREE.Mesh(geometry, material);
  scene.add(cube);

  // --- Luz ---
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 5, 5);
  scene.add(light);

  // --- Loop de renderização ---
  function render() {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

main();
