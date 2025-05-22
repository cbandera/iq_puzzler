"use client";

import React, { useEffect, useRef, useMemo, useState, ChangeEvent } from 'react';
import { Canvas, useThree, ThreeEvent } from '@react-three/fiber';
import { OrbitControls as DreiOrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';
import { PuzzleState } from '@/types/puzzle';
import { calculateCenterOfMass, validatePuzzleData } from '@/utils/puzzleUtils';
import { OrbitControls as OrbitControlsImpl } from 'three-stdlib';

const SPHERE_RADIUS = 0.5;

export interface PuzzleViewerProps {
  puzzleState: PuzzleState | null;
  zScale?: number;
}

export interface PieceLibraryItem {
  name: string;
  color: string;
  grid: boolean[];
}

function CoordinateAxes() {
  const axisOrigin = new THREE.Vector3(-2, -2, 0);

  return (
    <group position={[axisOrigin.x, axisOrigin.y, axisOrigin.z]}>
      {/* X axis - red */}
      <group>
        <mesh position={[1, 0, 0]} rotation={[0, 0, -Math.PI / 2]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="red" />
        </mesh>
        <Text position={[2.5, 0, 0]} color="red" fontSize={0.5} anchorX="center" anchorY="middle">X</Text>
      </group>
      {/* Y axis - green */}
      <group>
        <mesh position={[0, 1, 0]} rotation={[0, 0, 0]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="green" />
        </mesh>
        <Text position={[0, 2.5, 0]} color="green" fontSize={0.5} anchorX="center" anchorY="middle">Y</Text>
      </group>
      {/* Z axis - blue */}
      <group>
        <mesh position={[0, 0, 1]} rotation={[Math.PI / 2, 0, 0]}>
          <cylinderGeometry args={[0.05, 0.05, 2, 16]} />
          <meshStandardMaterial color="blue" />
        </mesh>
        <Text position={[0, 0, 2.5]} color="blue" fontSize={0.5} anchorX="center" anchorY="middle">Z</Text>
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
  const { camera, scene: threeScene } = useThree();
  const [resetKey, setResetKey] = useState(0);
  const controlsRef = useRef<OrbitControlsImpl>(null);

  useEffect(() => {
    threeScene.up.set(0, 0, 1);
  }, [threeScene]);

  const resetView = React.useCallback(() => {
    if (!camera) return;
    const distance = 15;
    camera.position.set(
      center.x,
      center.y - distance,
      center.z + distance * 0.7
    );
    camera.up.set(0, 0, 1);
    camera.lookAt(center);
    if (controlsRef.current) {
        controlsRef.current.update();
    }
    setResetKey(prev => prev + 1);
  }, [camera, center]);

  useEffect(() => {
    resetView();
  }, [resetView]); 

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
  }, [resetView]);

  const handleSphereClick = (event: ThreeEvent<MouseEvent>, positionKey: string) => {
    if (event.stopPropagation) {
      event.stopPropagation();
    }
    if (event.nativeEvent.shiftKey) {
      if (selectedPositions.includes(positionKey)) {
        setSelectedPositions(selectedPositions.filter(pos => pos !== positionKey));
      } else {
        setSelectedPositions([...selectedPositions, positionKey]);
      }
    } else {
      setSelectedPositions([positionKey]);
    }
  };

  return (
    <>
      <DreiOrbitControls
        key={resetKey}
        ref={controlsRef}
        target={center}
        makeDefault
      />
      <ambientLight intensity={0.7} />
      <pointLight position={[center.x + 10, center.y - 10, center.z + 10]} intensity={1.2} />
      <pointLight position={[center.x - 10, center.y + 10, center.z + 10]} intensity={0.8} color="#ffffff" />
      <directionalLight position={[0, 0, 10]} intensity={0.6} />
      <CoordinateAxes />
      {puzzleState && Object.entries(puzzleState).map(([key, position]) => {
        const isSelected = selectedPositions.includes(key);
        const material = position.occupied
          ? new THREE.MeshPhysicalMaterial({
            color: isSelected ? '#000000' : position.piece_color || '#ffffff',
            roughness: isSelected ? 0.3 : 0.1,
            metalness: 0.0,
            clearcoat: isSelected ? 0.5 : 0.3,
            clearcoatRoughness: 0.2,
            emissive: isSelected
              ? new THREE.Color(position.piece_color || '#ffffff')
              : new THREE.Color(position.piece_color || '#ffffff').multiplyScalar(0.15),
            emissiveIntensity: isSelected ? 0.7 : 0.2,
          })
          : new THREE.MeshPhysicalMaterial({
            color: isSelected ? '#000000' : '#808080',
            transparent: !isSelected,
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
              depthOffset={-1}
            >
              {key}
            </Text>
          </group>
        );
      })}
    </>
  );
}

export default function PuzzleViewer({ puzzleState: initialPuzzleState, zScale }: PuzzleViewerProps) {
  const [pieceLibrary, setPieceLibrary] = useState<PieceLibraryItem[]>([]);
  const [selectedPositions, setSelectedPositions] = useState<string[]>([]);
  const [modifiedPuzzleState, setModifiedPuzzleState] = useState<PuzzleState | null>(initialPuzzleState);
  const [isSolving, setIsSolving] = useState(false);
  const [solverOutput, setSolverOutput] = useState<string>('');
  const [showSolverOutput, setShowSolverOutput] = useState(false);

  useEffect(() => {
    fetch('/data/piece_library.json')
      .then(response => response.json())
      .then(data => setPieceLibrary(data))
      .catch(error => console.error('Failed to load piece library:', error));

    if (initialPuzzleState) {
      setModifiedPuzzleState({ ...initialPuzzleState });
    } else {
      setModifiedPuzzleState(null);
    }
  }, [initialPuzzleState]);

  useEffect(() => {
    if (initialPuzzleState) {
      setModifiedPuzzleState({ ...initialPuzzleState });
    } else {
      setModifiedPuzzleState(null);
    }
  }, [initialPuzzleState]);

  const center = useMemo(() => {
    if (!modifiedPuzzleState) return new THREE.Vector3(0, 0, 0);
    const com = calculateCenterOfMass(modifiedPuzzleState, zScale || 1);
    return new THREE.Vector3(com.x, com.y, com.z);
  }, [modifiedPuzzleState, zScale]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
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
        setModifiedPuzzleState(data);
      } catch (error) {
        alert('Error reading puzzle file. Please ensure it is a valid JSON file.');
        console.error('Error reading puzzle file:', error);
      }
    };
    reader.readAsText(file);
  };

  const resetToDefault = () => {
    if (initialPuzzleState) {
      setModifiedPuzzleState({ ...initialPuzzleState });
    } else {
      setModifiedPuzzleState(null);
    }
    setSelectedPositions([]);
    console.log('Reset to default puzzle state');
  };

  const solvePuzzle = async () => {
    if (!modifiedPuzzleState) return;
    try {
      setIsSolving(true);
      setSolverOutput('');
      setShowSolverOutput(true);
      const timestamp = new Date().getTime();
      const puzzleStateFilename = `puzzle-state-${timestamp}.json`;
      const solutionFilename = `solution-${timestamp}.json`;
      await exportPuzzleStateToFile(puzzleStateFilename);
      const response = await fetch('/api/solve-puzzle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          puzzleStateFile: puzzleStateFilename,
          libraryFile: 'piece_library.json',
          solutionFile: solutionFilename
        })
      });
      if (!response.ok) throw new Error(`Failed to start solver: ${response.statusText}`);
      const reader = response.body?.getReader();
      if (!reader) throw new Error('Failed to get response reader');
      let solutionFound = false;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = new TextDecoder().decode(value);
        const events = chunk.split('\n\n').filter(Boolean);
        for (const event of events) {
          if (event.startsWith('data: ')) {
            try {
              const data = JSON.parse(event.slice(5));
              if (data.output) {
                setSolverOutput(prev => prev + data.output);
                if (data.output.includes('Solution found!')) solutionFound = true;
              }
              if (data.completed && data.success && solutionFound) {
                await importSolution(solutionFilename);
              }
            } catch (e) { console.error('Error parsing event data:', e); }
          }
        }
      }
    } catch (error) {
      console.error('Error solving puzzle:', error);
      setSolverOutput(prev => prev + `\nError: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsSolving(false);
    }
  };

  const [localZScale, setLocalZScale] = useState(zScale || 1);

  useEffect(() => {
    const storedZScale = localStorage.getItem('zScale');
    if (storedZScale) setLocalZScale(parseFloat(storedZScale));
  }, []);

  useEffect(() => {
    if (zScale !== undefined) setLocalZScale(zScale);
  }, [zScale]);

  const updatePositionProperties = (pieceName: string | null, pieceColor: string | null) => {
    if (!modifiedPuzzleState || selectedPositions.length === 0) return;
    setSelectedPositions([]);
    const newState = { ...modifiedPuzzleState };
    selectedPositions.forEach(posKey => {
      newState[posKey] = {
        ...newState[posKey],
        occupied: pieceName !== null,
        piece_name: pieceName,
        piece_color: pieceColor
      };
    });
    setModifiedPuzzleState(newState);
  };

  const exportPuzzleState = () => {
    if (!modifiedPuzzleState) return;
    const dataStr = JSON.stringify(modifiedPuzzleState, null, 2);
    const dataUri = `data:application/json;charset=utf-8,${encodeURIComponent(dataStr)}`;
    const exportFileDefaultName = 'puzzle-state.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const exportPuzzleStateToFile = async (filename: string) => {
    if (!modifiedPuzzleState) throw new Error('No puzzle state to export');
    const dataStr = JSON.stringify(modifiedPuzzleState, null, 2);
    try {
      const blob = new Blob([dataStr], { type: 'application/json' });
      const formData = new FormData();
      formData.append('file', blob, filename);
      formData.append('path', 'data');
      formData.append('subdir', 'temp');
      const response = await fetch('/api/save-file', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) throw new Error(`Failed to save file: ${response.statusText}`);
      return await response.json();
    } catch (error) {
      console.error('Error saving puzzle state:', error);
      throw error;
    }
  };

  const importSolution = async (solutionFilename: string) => {
    try {
      const response = await fetch(`/data/temp/${solutionFilename}`);
      if (!response.ok) throw new Error(`Failed to load solution: ${response.statusText}`);
      const solutionData = await response.json();
      setModifiedPuzzleState(solutionData);
      return solutionData;
    } catch (error) {
      console.error('Error importing solution:', error);
      throw error;
    }
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
          <input type="file" accept=".json" onChange={handleFileChange} className="hidden" id="puzzle-import" />
          <button onClick={() => document.getElementById('puzzle-import')?.click()} className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600">Import</button>
          <button onClick={exportPuzzleState} className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600">Export</button>
          <button id="reset-view-button" className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600">Reset View</button>
          <button onClick={resetToDefault} className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600">Reset to Default</button>
          <button onClick={solvePuzzle} disabled={isSolving} className={`px-3 py-1 text-sm ${isSolving ? 'bg-gray-400' : 'bg-purple-600 hover:bg-purple-700'} text-white rounded flex items-center justify-center gap-2`}>
            {isSolving && <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>}
            {isSolving ? 'Solving...' : 'Solve'}
          </button>
        </div>
      </div>
      <Canvas className="w-full h-full">
        <Scene puzzleState={modifiedPuzzleState} zScale={localZScale} center={center} selectedPositions={selectedPositions} setSelectedPositions={setSelectedPositions} />
      </Canvas>
      {showSolverOutput && (
        <div className="fixed bottom-4 right-4 z-50 max-w-[800px] max-h-[60vh] w-[800px] bg-white bg-opacity-95 rounded-lg shadow-xl overflow-hidden border border-gray-300">
          <div className="flex justify-between items-center p-3 bg-gray-100 border-b border-gray-200">
            <div className="flex items-center">
              <h3 className="font-bold text-lg">Solver Output</h3>
              {isSolving && <div className="ml-3 flex items-center"><svg className="animate-spin h-4 w-4 text-purple-600 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg><span className="text-sm text-purple-600">Running...</span></div>}
            </div>
            <div className="flex gap-2"><button onClick={() => setShowSolverOutput(false)} className="p-1 rounded hover:bg-gray-200" title="Close">✕</button></div>
          </div>
          <div className="p-4 overflow-auto" style={{ maxHeight: 'calc(60vh - 56px)' }}><pre className="bg-gray-50 p-3 rounded overflow-auto whitespace-pre-wrap text-xs font-mono leading-relaxed">{solverOutput || 'No output available'}</pre></div>
        </div>
      )}
      {selectedPositions.length > 0 && modifiedPuzzleState && (
        <div className="absolute top-0 right-0 m-4 bg-white p-4 rounded shadow-lg w-80 max-h-[90vh] overflow-auto">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-bold">{selectedPositions.length === 1 ? `Position ${selectedPositions[0]}` : `${selectedPositions.length} Positions Selected`}</h3>
            <button onClick={() => setSelectedPositions([])} className="text-gray-500 hover:text-gray-700">✕</button>
          </div>
          <div className="mb-2">
            <h4 className="font-medium mb-1">Select Piece:</h4>
            <div className="grid grid-cols-2 gap-2">
              <div className="flex items-center p-1 border rounded cursor-pointer hover:bg-gray-100" onClick={() => updatePositionProperties(null, null)}><div className="w-5 h-5 mr-2 bg-gray-300 opacity-50 rounded"></div><span className="text-sm">Unoccupied</span></div>
              {pieceLibrary.map((piece, index) => (
                <div key={index} className="flex items-center p-1 border rounded cursor-pointer hover:bg-gray-100" onClick={() => updatePositionProperties(piece.name, piece.color)}><div className="w-5 h-5 mr-2 rounded" style={{ backgroundColor: piece.color }}></div><span className="text-sm">{piece.name}</span></div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
