import React, { useState, useEffect } from 'react'
import ReactFlow, { addEdge, Background, Controls, MiniMap } from 'react-flow-renderer'

export default function Flowchart() {
  const [elements, setElements] = useState<any[]>([])

  useEffect(() => {
    // load demo nodes
    setElements([
      { id: '1', data: { label: 'Hypothesis' }, position: { x: 0, y: 0 }, type: 'default' },
      { id: '2', data: { label: 'Aim 1' }, position: { x: 200, y: 0 }, type: 'default' },
    ])
  }, [])

  const onConnect = (params: any) => setElements((els) => addEdge(params, els))

  return (
    <div style={{ height: 400, border: '1px solid #eee' }}>
      <ReactFlow elements={elements} onConnect={onConnect}>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  )
}
