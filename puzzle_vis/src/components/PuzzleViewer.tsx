import { useRef, useState, useMemo, useEffect } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { PuzzleState } from '@/types/puzzle'
import * as THREE from 'three'

interface PuzzleViewerProps {
  puzzleState: PuzzleState | null;
  sphereRadius: number;
  zScale: number;
}

function calculateCenterOfMass(puzzleState: PuzzleState, zScale: number) {
  const positions = Object.values(puzzleState).map(pos => ({
    ...pos.coordinate,
    z: pos.coordinate.z * zScale
  }));
  const sum = positions.reduce(
    (acc, coord) => ({
      x: acc.x + coord.x,
      y: acc.y + coord.y,
      z: acc.z + coord.z
    }),
    { x: 0, y: 0, z: 0 }
  );
  
  return {
    x: sum.x / positions.length,
    y: sum.y / positions.length,
    z: sum.z / positions.length
  };
}

function Scene({ puzzleState, sphereRadius, zScale, center }: PuzzleViewerProps & { center: THREE.Vector3 }) {
  const { camera, scene } = useThree();
  const [resetKey, setResetKey] = useState(0);
  
  // Set up scene orientation
  useEffect(() => {
    // Set z-axis as up for the entire scene
    scene.up.set(0, 0, 1);
  }, [scene]);

  // Function to reset camera to default position
  const resetView = () => {
    if (!camera) return;
    const distance = 15;
    camera.position.set(
      center.x, // Same x as center
      center.y - distance, // Behind center (negative y)
      center.z + distance * 0.7 // Above center (positive z)
    );
    camera.up.set(0, 0, 1);
    camera.lookAt(center);
    // Force OrbitControls to re-render with new position
    setResetKey(prev => prev + 1);
  };

  // Update camera position and orientation on mount and when center changes
  useEffect(() => {
    resetView();
  }, [camera, center]);

  // Expose resetView to parent component
  useEffect(() => {
    const element = document.getElementById('reset-view-button');
    if (element) {
      element.onclick = resetView;
    }
    return () => {
      if (element) {
        element.onclick = null;
      }
    };
  }, [camera, center]);

  return (
    <>
      <OrbitControls 
        key={resetKey}
        target={center}
        makeDefault
      />
      <ambientLight intensity={0.5} />
      <pointLight position={[center.x + 10, center.y - 10, center.z + 10]} intensity={1} />
      {puzzleState && Object.entries(puzzleState).map(([key, position]) => {
        const material = position.occupied
          ? new THREE.MeshStandardMaterial({
              color: position.piece_color || '#ffffff',
              roughness: 0.3,
              metalness: 0.1,
            })
          : new THREE.MeshStandardMaterial({
              color: '#808080',
              transparent: true,
              opacity: 0.3,
              roughness: 0.3,
              metalness: 0.1,
            });

        return (
          <mesh
            key={key}
            position={[
              position.coordinate.x,
              position.coordinate.y,
              position.coordinate.z * zScale
            ]}
          >
            <sphereGeometry args={[sphereRadius, 32, 32]} />
            <primitive object={material} attach="material" />
          </mesh>
        );
      })}
    </>
  );
}

export default function PuzzleViewer({ puzzleState, sphereRadius, zScale }: PuzzleViewerProps) {
  const center = useMemo(() => {
    if (!puzzleState) return new THREE.Vector3(0, 0, 0);
    const com = calculateCenterOfMass(puzzleState, zScale);
    return new THREE.Vector3(com.x, com.y, com.z);
  }, [puzzleState, zScale]);

  return (
    <div className="w-full h-[600px] relative">
      <button
        id="reset-view-button"
        className="absolute top-4 right-4 px-3 py-1 bg-white/80 hover:bg-white text-gray-800 rounded shadow-md z-10 text-sm font-medium"
      >
        Reset View
      </button>
      <Canvas camera={{ fov: 50 }}>
        {puzzleState && (
          <Scene
            puzzleState={puzzleState}
            sphereRadius={sphereRadius}
            zScale={zScale}
            center={center}
          />
        )}
      </Canvas>
    </div>
  );
}
