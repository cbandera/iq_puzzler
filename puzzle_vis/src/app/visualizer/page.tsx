import { useEffect, useRef, useMemo, useState } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import { PuzzleState } from '@/types/puzzle'
import { calculateCenterOfMass, validatePuzzleData } from '@/utils/puzzleUtils';

const SPHERE_RADIUS = 0.5;

interface PuzzleViewerProps {
  puzzleState: PuzzleState | null;
  zScale?: number;
}

function Scene({ puzzleState, zScale, center }: PuzzleViewerProps & { center: THREE.Vector3 }) {
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
              position.coordinate.z * (zScale || 1)
            ]}
          >
            <sphereGeometry args={[SPHERE_RADIUS, 32, 32]} />
            <primitive object={material} attach="material" />
          </mesh>
        );
      })}
    </>
  );
}

export default function PuzzleViewer({ puzzleState, zScale }: PuzzleViewerProps) {
  const center = useMemo(() => {
    if (!puzzleState) return new THREE.Vector3(0, 0, 0);
    const com = calculateCenterOfMass(puzzleState, zScale || 1);
    return new THREE.Vector3(com.x, com.y, com.z);
  }, [puzzleState, zScale]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result;
      if (typeof content !== 'string') return;
      
      try {
        const data = JSON.parse(content);
        if (!validatePuzzleData(data)) {
          alert('Invalid puzzle data format. Please check the file structure.');
          return;
        }
        // Handle the imported data
        console.log('Imported puzzle data:', data);
      } catch (error) {
        alert('Error reading puzzle file. Please ensure it is a valid JSON file.');
        console.error('Error reading puzzle file:', error);
      }
    };
    reader.readAsText(file);
  };

  const resetToDefault = () => {
    // Add reset functionality here
    console.log('Resetting to default puzzle state');
  };

  const [localZScale, setLocalZScale] = useState(zScale || 1);

  useEffect(() => {
    const storedZScale = localStorage.getItem('zScale');
    if (storedZScale) {
      setLocalZScale(parseFloat(storedZScale));
    }
  }, []);

  useEffect(() => {
    if (zScale !== undefined) {
      setLocalZScale(zScale);
    }
  }, [zScale]);

  return (
    <div className="w-full h-[600px] relative">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <label htmlFor="zscale-slider" className="text-sm font-medium">
              Z-axis Scale: {localZScale}
            </label>
            <input
              id="zscale-slider"
              type="range"
              min="1"
              max="5"
              step="0.1"
              value={localZScale}
              onChange={(e) => {
                const value = parseFloat(e.target.value);
                localStorage.setItem('zScale', value.toString());
                setLocalZScale(value);
              }}
              className="w-32"
            />
          </div>
        </div>
        <div className="flex gap-2">
          <input 
            type="file" 
            accept=".json"
            onChange={handleFileChange}
            className="hidden"
            id="puzzle-import"
          />
          <button
            onClick={() => document.getElementById('puzzle-import')?.click()}
            className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Import
          </button>
          <button
            id="reset-view-button"
            className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Reset View
          </button>
          <button
            onClick={resetToDefault}
            className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            Reset to Default
          </button>
        </div>
      </div>
      <Canvas camera={{ fov: 50 }}>
        {puzzleState && (
          <Scene
            puzzleState={puzzleState}
            zScale={localZScale}
            center={center}
          />
        )}
      </Canvas>
    </div>
  );
}
