import { useEffect, useRef, useMemo, useState } from 'react'
import { Canvas, useThree, extend, ThreeEvent } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'
import * as THREE from 'three'
import { PuzzleState, Position } from '@/types/puzzle'
import { calculateCenterOfMass, validatePuzzleData } from '@/utils/puzzleUtils';

const SPHERE_RADIUS = 0.5;

interface PuzzleViewerProps {
  puzzleState: PuzzleState | null;
  zScale?: number;
}

interface PieceLibraryItem {
  name: string;
  color: string;
  grid: boolean[];
}

function CoordinateAxes() {
  const axisOrigin = new THREE.Vector3(-2, -2, 0);

  return (
    <group position={[axisOrigin.x, axisOrigin.y, axisOrigin.z]}>
      {/* All axes originate from the same point */}

      {/* X axis - red */}
      <group>
        <mesh position={[1, 0, 0]} rotation={[0, 0, -Math.PI / 2]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="red" />
        </mesh>
        <Text
          position={[2.5, 0, 0]}
          color="red"
          fontSize={0.5}
          anchorX="center"
          anchorY="middle"
        >
          X
        </Text>
      </group>

      {/* Y axis - green */}
      <group>
        <mesh position={[0, 1, 0]} rotation={[0, 0, 0]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="green" />
        </mesh>
        <Text
          position={[0, 2.5, 0]}
          color="green"
          fontSize={0.5}
          anchorX="center"
          anchorY="middle"
        >
          Y
        </Text>
      </group>

      {/* Z axis - blue */}
      <group>
        <mesh position={[0, 0, 1]} rotation={[Math.PI / 2, 0, 0]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="blue" />
        </mesh>
        <Text
          position={[0, 0, 2.5]}
          color="blue"
          fontSize={0.5}
          anchorX="center"
          anchorY="middle"
        >
          Z
        </Text>
      </group>

      {/* Origin sphere */}
      <mesh>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshStandardMaterial color="white" />
      </mesh>
    </group>
  );
}

function Scene({
  puzzleState,
  zScale,
  center,
  selectedPosition,
  setSelectedPosition
}: PuzzleViewerProps & {
  center: THREE.Vector3,
  selectedPosition: string | null,
  setSelectedPosition: (position: string | null) => void
}) {
  const { camera, scene } = useThree();
  const [resetKey, setResetKey] = useState(0);
  const controlsRef = useRef(null);

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
  // Only reset the view when the component first mounts, not on re-renders
  useEffect(() => {
    resetView();
    // Only run once on mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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

  // Handle sphere click
  const handleSphereClick = (event: ThreeEvent<MouseEvent>, positionKey: string) => {
    // Use ThreeEvent from THREE.js (typed as any here for simplicity)
    if (event.stopPropagation) {
      event.stopPropagation();
    }
    setSelectedPosition(positionKey);
  };

  return (
    <>
      <OrbitControls
        key={resetKey}
        ref={controlsRef}
        target={center}
        makeDefault
      />
      <ambientLight intensity={0.5} />
      <pointLight position={[center.x + 10, center.y - 10, center.z + 10]} intensity={1} />

      {/* Coordinate axes positioned near the spheres */}
      <CoordinateAxes />

      {/* Spheres for puzzle positions */}
      {puzzleState && Object.entries(puzzleState).map(([key, position]) => {
        const isSelected = key === selectedPosition;

        const material = position.occupied
          ? new THREE.MeshStandardMaterial({
            color: position.piece_color || '#ffffff',
            roughness: 0.3,
            metalness: 0.1,
            emissive: isSelected ? new THREE.Color(0x555555) : undefined,
          })
          : new THREE.MeshStandardMaterial({
            color: '#808080',
            transparent: true,
            opacity: 0.3,
            roughness: 0.3,
            metalness: 0.1,
            emissive: isSelected ? new THREE.Color(0x555555) : undefined,
          });

        return (
          <group key={key}>
            <mesh
              position={[
                position.coordinate.x,
                position.coordinate.y,
                position.coordinate.z * (zScale || 1)
              ]}
              onClick={(e) => handleSphereClick(e, key)}
            >
              <sphereGeometry args={[SPHERE_RADIUS, 32, 32]} />
              <primitive object={material} attach="material" />
            </mesh>

            {/* Position index label */}
            <Text
              position={[
                position.coordinate.x,
                position.coordinate.y,
                position.coordinate.z * (zScale || 1)
              ]}
              color="black"
              fontSize={0.25}
              anchorX="center"
              anchorY="middle"
              depthOffset={-1} // Ensure text is visible in front of sphere
            >
              {key}
            </Text>
          </group>
        );
      })}
    </>
  );
}

export default function PuzzleViewer({ puzzleState, zScale }: PuzzleViewerProps) {
  const [pieceLibrary, setPieceLibrary] = useState<PieceLibraryItem[]>([]);
  const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
  const [modifiedPuzzleState, setModifiedPuzzleState] = useState<PuzzleState | null>(puzzleState);

  // Fetch piece library on component mount
  useEffect(() => {
    fetch('/data/piece_library.json')
      .then(response => response.json())
      .then(data => setPieceLibrary(data))
      .catch(error => console.error('Failed to load piece library:', error));

    // Initialize modifiedPuzzleState from puzzleState
    if (puzzleState) {
      setModifiedPuzzleState({ ...puzzleState });
    }
  }, [puzzleState]);

  // When puzzleState changes externally, update modifiedPuzzleState
  useEffect(() => {
    if (puzzleState) {
      setModifiedPuzzleState({ ...puzzleState });
    }
  }, [puzzleState]);

  const center = useMemo(() => {
    if (!modifiedPuzzleState) return new THREE.Vector3(0, 0, 0);
    const com = calculateCenterOfMass(modifiedPuzzleState, zScale || 1);
    return new THREE.Vector3(com.x, com.y, com.z);
  }, [modifiedPuzzleState, zScale]);

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
        // Update puzzle state with imported data
        setModifiedPuzzleState(data);
      } catch (error) {
        alert('Error reading puzzle file. Please ensure it is a valid JSON file.');
        console.error('Error reading puzzle file:', error);
      }
    };
    reader.readAsText(file);
  };

  const resetToDefault = () => {
    // Reset to original puzzle state
    if (puzzleState) {
      setModifiedPuzzleState({ ...puzzleState });
    }
    setSelectedPosition(null);
    console.log('Reset to default puzzle state');
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

  // Update position properties
  const updatePositionProperties = (pieceName: string | null, pieceColor: string | null) => {
    if (!selectedPosition || !modifiedPuzzleState) return;

    const newState = { ...modifiedPuzzleState };
    newState[selectedPosition] = {
      ...newState[selectedPosition],
      occupied: pieceName !== null,
      piece_name: pieceName,
      piece_color: pieceColor
    };

    setModifiedPuzzleState(newState);

    // Close the dialog once a piece/color is selected
    setSelectedPosition(null);
  };

  // Export puzzle state to JSON file
  const exportPuzzleState = () => {
    if (!modifiedPuzzleState) return;

    const dataStr = JSON.stringify(modifiedPuzzleState, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

    const exportFileDefaultName = `puzzle-state-${new Date().toISOString().slice(0, 10)}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

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
            onClick={exportPuzzleState}
            className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600"
          >
            Export
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

      {/* 3D Canvas */}
      <Canvas className="w-full h-full">
        <Scene
          puzzleState={modifiedPuzzleState}
          zScale={localZScale}
          center={center}
          selectedPosition={selectedPosition}
          setSelectedPosition={setSelectedPosition}
        />
      </Canvas>

      {/* Selection dialog */}
      {selectedPosition && modifiedPuzzleState && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded shadow-lg w-72">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold">Position {selectedPosition}</h3>
            <button
              onClick={() => setSelectedPosition(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <div className="mb-4">
            <h4 className="font-medium mb-2">Select Piece:</h4>
            <div className="flex flex-col gap-2 max-h-60 overflow-y-auto">
              <div
                className="flex items-center p-2 border rounded cursor-pointer hover:bg-gray-100"
                onClick={() => updatePositionProperties(null, null)}
              >
                <div className="w-6 h-6 mr-2 bg-gray-300 opacity-50 rounded"></div>
                <span>Unoccupied</span>
              </div>

              {pieceLibrary.map((piece, index) => (
                <div
                  key={index}
                  className="flex items-center p-2 border rounded cursor-pointer hover:bg-gray-100"
                  onClick={() => updatePositionProperties(piece.name, piece.color)}
                >
                  <div
                    className="w-6 h-6 mr-2 rounded"
                    style={{ backgroundColor: piece.color }}
                  ></div>
                  <span>{piece.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
