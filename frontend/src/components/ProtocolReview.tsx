import React, { useState } from 'react'

export default function ProtocolReview() {
  const [videoId, setVideoId] = useState('')
  const [protocol, setProtocol] = useState<any | null>(null)
  const [editingSteps, setEditingSteps] = useState<any[]>([])
  const [experimentId, setExperimentId] = useState('demo-experiment')

  async function load() {
    if (!videoId) return
    const r = await fetch(`/api/videos/${videoId}/synthesize-structured`, { method: 'POST' })
    if (r.ok) {
      const j = await r.json()
      setProtocol(j)
      setEditingSteps(j.steps ?? [])
    } else {
      setProtocol(null)
      setEditingSteps([])
      alert('Failed to synthesize structured protocol')
    }
  }

  function updateStep(idx: number, field: string, value: string) {
    const s = [...editingSteps]
    s[idx] = { ...s[idx], [field]: value }
    setEditingSteps(s)
  }

  async function saveCorrections() {
    const corrected = { steps: editingSteps, reagents: protocol?.reagents ?? [], equipment: protocol?.equipment ?? [] }
    const md = '# Corrected Protocol\n\n' + editingSteps.map((s, i) => `${i+1}. ${s.action} - ${s.details}`).join('\n')
    const r = await fetch('/api/labels/correction', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ video_id: videoId, experiment_id: experimentId, corrected_protocol: corrected, corrected_markdown: md }) })
    if (r.ok) {
      const j = await r.json()
      alert('Saved correction: ' + j.id)
    } else {
      alert('Save failed')
    }
  }

  return (
    <div>
      <h3>Protocol Review</h3>
      <input placeholder="video id" value={videoId} onChange={e => setVideoId(e.target.value)} style={{ width: '100%', marginBottom: 8 }} />
      <button onClick={load} disabled={!videoId}>Load Structured Protocol</button>

      {editingSteps.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <h4>Steps</h4>
          {editingSteps.map((s, idx) => (
            <div key={idx} style={{ marginBottom: 8, padding: 8, border: '1px solid #eee' }}>
              <input value={s.action} onChange={e => updateStep(idx, 'action', e.target.value)} style={{ width: '100%', marginBottom: 6 }} />
              <textarea value={s.details} onChange={e => updateStep(idx, 'details', e.target.value)} rows={3} style={{ width: '100%' }} />
            </div>
          ))}
          <button onClick={saveCorrections}>Save Corrections</button>
        </div>
      )}
    </div>
  )
}
