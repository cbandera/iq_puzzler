import { PuzzleState } from '@/types/puzzle';

export function calculateCenterOfMass(puzzleState: PuzzleState, zScale: number) {
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

export function validatePuzzleData(data: unknown): data is PuzzleState {
  if (!data || typeof data !== 'object') return false;
  
  for (const [, value] of Object.entries(data)) {
    if (!value || typeof value !== 'object') return false;
    if (!('occupied' in value) || typeof value.occupied !== 'boolean') return false;
    if ('piece_color' in value && value.piece_color !== null && typeof value.piece_color !== 'string') return false;
    if (!('coordinate' in value) || !value.coordinate || typeof value.coordinate !== 'object') return false;
    
    const coord = value.coordinate;
    if (!('x' in coord) || typeof coord.x !== 'number') return false;
    if (!('y' in coord) || typeof coord.y !== 'number') return false;
    if (!('z' in coord) || typeof coord.z !== 'number') return false;
  }
  
  return true;
}
