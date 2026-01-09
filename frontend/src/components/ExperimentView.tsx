import React, { useState } from 'react'

export default function ExperimentView() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [experimentId, setExperimentId] = useState<string | null>('demo-experiment')
  const [protocol, setProtocol] = useState<string | null>(null)
  const [editing, setEditing] = useState<boolean>(false)
  const [editText, setEditText] = useState<string | null>(null)

  async function synth() {
    if (!videoId) return
    const res = await fetch(`/api/videos/${videoId}/synthesize`, { method: 'POST' })
    if (res.ok) {
      const j = await res.json()
      setProtocol(j.protocol_markdown)
      setEditText(j.protocol_markdown)
      setEditing(true)
    } else {
      setProtocol('Synthesis failed')
    }
  }

  async function saveProtocol() {
    if (!experimentId || !editText) return
    const res = await fetch(`/api/protocols/experiment/${experimentId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_markdown: editText, generated_by_video_id: videoId })
    })
    if (res.ok) {
      const j = await res.json()
      alert('Protocol saved: ' + j.id)
      setEditing(false)
    } else {
      alert('Save failed')
    }
  }

  return (
    <div>
      <h3>Experiment</h3>
      <input placeholder="experiment id" value={experimentId ?? ''} onChange={e => setExperimentId(e.target.value)} style={{ width: '100%', marginBottom: 8 }} />
      <input placeholder="video id" onChange={e => setVideoId(e.target.value)} style={{ width: '100%', marginBottom: 8 }} />
      <button onClick={synth} disabled={!videoId}>Synthesize Protocol</button>
      {editing && (
        <div style={{ marginTop: 12 }}>
          <h4>Protocol (edit)</h4>
          <textarea value={editText ?? ''} onChange={e => setEditText(e.target.value)} rows={10} style={{ width: '100%' }} />
          <button onClick={saveProtocol} style={{ marginTop: 8 }}>Save Protocol</button>
        </div>
      )}
      {protocol && !editing && (
        <div style={{ marginTop: 12 }}>
          <h4>Protocol</h4>
          <pre>{protocol}</pre>
        </div>
      )}
    </div>
  )
}
