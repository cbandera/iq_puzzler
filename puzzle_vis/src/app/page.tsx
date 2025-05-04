'use client'
import { useState, useEffect } from 'react'
import { PuzzleState } from '@/types/puzzle'
import PuzzleViewer from './visualizer/page';

const DEFAULT_SOLUTION_PATH = '/data/solution.json';

export default function Home() {
  const [puzzleState, setPuzzleState] = useState<PuzzleState | null>(null)
  const [zScale, setZScale] = useState<number>(1)

  // Load state from localStorage or default solution on mount
  useEffect(() => {
    const savedState = localStorage.getItem('puzzleState')
    const savedZScale = localStorage.getItem('zScale')

    if (savedState) {
      setPuzzleState(JSON.parse(savedState))
    } else {
      // Load default solution
      fetch(DEFAULT_SOLUTION_PATH)
        .then(response => response.json())
        .then(data => {
          setPuzzleState(data)
          localStorage.setItem('puzzleState', JSON.stringify(data))
        })
        .catch(error => console.error('Error loading default solution:', error))
    }

    if (savedZScale) {
      setZScale(parseFloat(savedZScale))
    }
  }, [])

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold">IQ Puzzler Visualizer</h1>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <PuzzleViewer
            puzzleState={puzzleState}
            zScale={zScale}
          />
        </div>
      </div>
    </main>
  )
}
