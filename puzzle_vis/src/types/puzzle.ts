export interface Coordinate {
  x: number;
  y: number;
  z: number;
}

export interface Position {
  coordinate: Coordinate;
  occupied: boolean;
  piece_name: string | null;
  piece_color: string | null;
}

export interface PuzzleState {
  [key: string]: Position;
}
