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
  selectedPositions,
  setSelectedPositions
}: PuzzleViewerProps & {
  center: THREE.Vector3,
  selectedPositions: string[],
  setSelectedPositions: (positions: string[]) => void
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

  // Handle sphere click with multi-select support
  const handleSphereClick = (event: ThreeEvent<MouseEvent>, positionKey: string) => {
    // Use ThreeEvent from THREE.js
    if (event.stopPropagation) {
      event.stopPropagation();
    }
    
    // Check if shift key is pressed for multi-select
    if (event.nativeEvent.shiftKey) {
      // If already selected, remove it; otherwise add it
      if (selectedPositions.includes(positionKey)) {
        setSelectedPositions(selectedPositions.filter(pos => pos !== positionKey));
      } else {
        setSelectedPositions([...selectedPositions, positionKey]);
      }
    } else {
      // Normal click (no shift) - select only this position
      setSelectedPositions([positionKey]);
    }
  };

  return (
    <>
      <OrbitControls
        key={resetKey}
        ref={controlsRef}
        target={center}
        makeDefault
      />
      {/* Enhanced lighting setup for more vibrant colors */}
      <ambientLight intensity={0.7} />
      <pointLight position={[center.x + 10, center.y - 10, center.z + 10]} intensity={1.2} />
      <pointLight position={[center.x - 10, center.y + 10, center.z + 10]} intensity={0.8} color="#ffffff" />
      <directionalLight position={[0, 0, 10]} intensity={0.6} />

      {/* Coordinate axes positioned near the spheres */}
      <CoordinateAxes />

      {/* Spheres for puzzle positions */}
      {puzzleState && Object.entries(puzzleState).map(([key, position]) => {
        const isSelected = selectedPositions.includes(key);

        // Enhanced material settings with more pronounced selection highlighting
        const material = position.occupied
          ? new THREE.MeshPhysicalMaterial({
            // If selected, make the sphere black with the original color as emissive
            color: isSelected ? '#000000' : position.piece_color || '#ffffff',
            roughness: isSelected ? 0.3 : 0.1,  // Rougher when selected
            metalness: 0.0,                     // No metalness for brighter colors
            clearcoat: isSelected ? 0.5 : 0.3,  // More clearcoat when selected
            clearcoatRoughness: 0.2,
            // Use original color as emissive when selected for a glowing effect
            emissive: isSelected 
              ? new THREE.Color(position.piece_color || '#ffffff') 
              : new THREE.Color(position.piece_color || '#ffffff').multiplyScalar(0.15),
            emissiveIntensity: isSelected ? 0.7 : 0.2,
          })
          : new THREE.MeshPhysicalMaterial({
            color: isSelected ? '#000000' : '#808080',
            transparent: !isSelected,           // Not transparent when selected
            opacity: isSelected ? 1.0 : 0.3,
            roughness: isSelected ? 0.3 : 0.2,
            metalness: 0.0,
            clearcoat: isSelected ? 0.5 : 0.1,
            emissive: isSelected ? new THREE.Color('#ffffff') : undefined,
            emissiveIntensity: isSelected ? 0.3 : 0,
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
  // Replace single selection with array of selections
  const [selectedPositions, setSelectedPositions] = useState<string[]>([]);
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
    setSelectedPositions([]);
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

  // Function to update position properties for all selected positions
  const updatePositionProperties = (pieceName: string | null, pieceColor: string | null) => {
    if (!modifiedPuzzleState || selectedPositions.length === 0) return;

    // Close the dialog once a piece/color is selected
    setSelectedPositions([]);

    // Clone the current state
    const newState = { ...modifiedPuzzleState };

    // Update all selected positions with the same piece/color
    selectedPositions.forEach(posKey => {
      newState[posKey] = {
        ...newState[posKey],
        occupied: pieceName !== null,
        piece_name: pieceName,
        piece_color: pieceColor
      };
    });

    // Update the state
    setModifiedPuzzleState(newState);
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
          selectedPositions={selectedPositions}
          setSelectedPositions={setSelectedPositions}
        />
      </Canvas>

      {/* Selection dialog - Moved to the right side to avoid occluding the view */}
      {selectedPositions.length > 0 && modifiedPuzzleState && (
        <div className="absolute top-0 right-0 m-4 bg-white p-4 rounded shadow-lg w-80 max-h-[90vh] overflow-auto">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-bold">
              {selectedPositions.length === 1 
                ? `Position ${selectedPositions[0]}` 
                : `${selectedPositions.length} Positions Selected`}
            </h3>
            <button
              onClick={() => setSelectedPositions([])}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <div className="mb-2">
            <h4 className="font-medium mb-1">Select Piece:</h4>
            <div className="grid grid-cols-2 gap-2">
              <div
                className="flex items-center p-1 border rounded cursor-pointer hover:bg-gray-100"
                onClick={() => updatePositionProperties(null, null)}
              >
                <div className="w-5 h-5 mr-2 bg-gray-300 opacity-50 rounded"></div>
                <span className="text-sm">Unoccupied</span>
              </div>

              {pieceLibrary.map((piece, index) => (
                <div
                  key={index}
                  className="flex items-center p-1 border rounded cursor-pointer hover:bg-gray-100"
                  onClick={() => updatePositionProperties(piece.name, piece.color)}
                >
                  <div
                    className="w-5 h-5 mr-2 rounded"
                    style={{ backgroundColor: piece.color }}
                  ></div>
                  <span className="text-sm">{piece.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
