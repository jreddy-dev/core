import React, { useState, useEffect } from 'react'
import { Box, Input, Button, VStack, HStack, Text, Badge } from '@chakra-ui/react'

export default function ExperimentView() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [experimentId, setExperimentId] = useState<string | null>('demo-experiment')
  const [protocol, setProtocol] = useState<string | null>(null)
  const [editing, setEditing] = useState<boolean>(false)
  const [editText, setEditText] = useState<string | null>(null)
  const [videos, setVideos] = useState<any[]>([])

  useEffect(() => {
    async function load() {
      if (!experimentId) return
      try {
        const r = await fetch(`/api/experiments/${experimentId}/videos`)
        if (r.ok) {
          const j = await r.json()
          setVideos(j)
        }
      } catch (e) {}
    }
    load()
  }, [experimentId])

  async function synthFor(videoIdLocal: string) {
    const res = await fetch(`/api/videos/${videoIdLocal}/synthesize`, { method: 'POST' })
    if (res.ok) {
      const j = await res.json()
      setProtocol(j.protocol_markdown)
      setEditText(j.protocol_markdown)
      setEditing(true)
      setVideoId(videoIdLocal)
    } else {
      setProtocol('Synthesis failed')
    }
  }

  async function saveProtocol() {
    if (!experimentId || !editText || !videoId) return
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
    <Box mt={4}>
      <Text fontWeight="bold">Experiment</Text>
      <Input placeholder="experiment id" value={experimentId ?? ''} onChange={e => setExperimentId(e.target.value)} mt={2} />

      <Box mt={3}>
        <Text fontSize="sm" fontWeight="semibold">Videos</Text>
        <VStack spacing={2} align="stretch" mt={2}>
          {videos.length === 0 && <Text>No videos yet</Text>}
          {videos.map(v => (
            <HStack key={v.id} justify="space-between">
              <Text><code>{v.id}</code></Text>
              <HStack>
                <Badge colorScheme={v.status === 'processed' ? 'green' : 'yellow'}>{v.status}</Badge>
                <Button size="sm" onClick={() => synthFor(v.id)}>Synthesize</Button>
                <a href={`/api/downloads/${v.id}`}>Download</a>
              </HStack>
            </HStack>
          ))}
        </VStack>
      </Box>

      {editing && (
        <Box mt={4}>
          <Text fontWeight="semibold">Protocol (edit)</Text>
          <textarea value={editText ?? ''} onChange={e => setEditText(e.target.value)} rows={8} style={{ width: '100%' }} />
          <Button mt={2} onClick={saveProtocol}>Save Protocol</Button>
        </Box>
      )}

      {protocol && !editing && (
        <Box mt={4}>
          <Text fontWeight="semibold">Protocol (preview)</Text>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{protocol}</pre>
        </Box>
      )}
    </Box>
  )
}
