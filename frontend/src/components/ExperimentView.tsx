import React, { useState } from 'react'

export default function ExperimentView() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [protocol, setProtocol] = useState<string | null>(null)

  async function synth() {
    if (!videoId) return
    const res = await fetch(`/api/videos/${videoId}/synthesize`, { method: 'POST' })
    if (res.ok) {
      const j = await res.json()
      setProtocol(j.protocol_markdown)
    } else {
      setProtocol('Synthesis failed')
    }
  }

  return (
    <div>
      <h3>Experiment</h3>
      <input placeholder="video id" onChange={e => setVideoId(e.target.value)} />
      <button onClick={synth} disabled={!videoId}>Synthesize Protocol</button>
      {protocol && (
        <div style={{ marginTop: 12 }}>
          <h4>Protocol</h4>
          <pre>{protocol}</pre>
        </div>
      )}
    </div>
  )
}
