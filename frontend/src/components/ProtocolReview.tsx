import React, { useState } from 'react'
import { Box, Input, Button, VStack, HStack, Text, Textarea } from '@chakra-ui/react'
import ReactMarkdown from 'react-markdown'

export default function ProtocolReview() {
  const [videoId, setVideoId] = useState('')
  const [protocol, setProtocol] = useState<any | null>(null)
  const [editingSteps, setEditingSteps] = useState<any[]>([])
  const [experimentId, setExperimentId] = useState('demo-experiment')
  const [previewMode, setPreviewMode] = useState(false)

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
      alert('Saved correction: ' + j.protocol_version_id)
    } else {
      alert('Save failed')
    }
  }

  return (
    <Box mt={4}>
      <Text fontWeight="bold">Protocol Review</Text>
      <Input placeholder="video id" value={videoId} onChange={e => setVideoId(e.target.value)} mt={2} />
      <HStack mt={2}>
        <Button size="sm" onClick={load} isDisabled={!videoId}>Load Structured Protocol</Button>
        <Button size="sm" variant="ghost" onClick={() => setPreviewMode(!previewMode)}>{previewMode ? 'Edit' : 'Preview'}</Button>
      </HStack>

      {editingSteps.length > 0 && !previewMode && (
        <Box mt={3}>
          <VStack spacing={3} align="stretch">
            {editingSteps.map((s, idx) => (
              <Box key={idx} p={3} borderWidth={1} borderRadius="md">
                <Input value={s.action} onChange={e => updateStep(idx, 'action', e.target.value)} mb={2} />
                <Textarea value={s.details} onChange={e => updateStep(idx, 'details', e.target.value)} rows={3} />
              </Box>
            ))}
            <Button onClick={saveCorrections}>Save Corrections</Button>
          </VStack>
        </Box>
      )}

      {previewMode && editingSteps.length > 0 && (
        <Box mt={3} borderWidth={1} p={3} borderRadius="md">
          <ReactMarkdown>{'# Protocol\n\n' + editingSteps.map((s, i) => `${i+1}. **${s.action}** - ${s.details}`).join('\n')}</ReactMarkdown>
        </Box>
      )}
    </Box>
  )
}
