import React, { useState } from 'react'
import { Box, Input, Button, Checkbox, Progress, Text, HStack, Badge } from '@chakra-ui/react'

export default function VideoUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [consent, setConsent] = useState(false)
  const [uploadId, setUploadId] = useState<string | null>(null)

  function upload() {
    if (!file) return
    setUploading(true)
    setProgress(0)

    const xhr = new XMLHttpRequest()
    const url = `/api/videos/demo-experiment?consent=${consent ? 'true' : 'false'}`
    xhr.open('POST', url)
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        setProgress(Math.round((e.loaded / e.total) * 100))
      }
    }
    xhr.onload = () => {
      setUploading(false)
      if (xhr.status === 201) {
        const j = JSON.parse(xhr.responseText)
        setStatus('Uploaded')
        setUploadId(j.id)
        // start polling
        const poll = async () => {
          try {
            const r = await fetch(`/api/videos/${j.id}`)
            if (r.ok) {
              const data = await r.json()
              setStatus(`status: ${data.status}`)
              if (data.status === 'processed' || data.status === 'failed') return
              setTimeout(poll, 2000)
            }
          } catch (e) {
            setStatus('Status fetch error')
          }
        }
        poll()
      } else {
        setStatus('Upload failed')
      }
    }
    const fd = new FormData()
    fd.append('file', file)
    xhr.send(fd)
  }

  return (
    <Box>
      <Text fontWeight="bold">Upload lab video</Text>
      <Input type="file" accept="video/*" onChange={e => setFile(e.target.files?.[0] ?? null)} />
      <HStack mt={2} spacing={4}>
        <Checkbox isChecked={consent} onChange={e => setConsent(e.target.checked)}>Allow this video to be used to improve models</Checkbox>
        <Button colorScheme="blue" onClick={upload} isDisabled={!file || uploading}>
          {uploading ? 'Uploading...' : 'Upload'}
        </Button>
      </HStack>

      {uploading && <Progress value={progress} mt={3} size="sm" />}

      {status && (
        <Box mt={3}>
          <Badge colorScheme={status.includes('processed') ? 'green' : 'yellow'}>{status}</Badge>
          {uploadId && <Text mt={2}>Video id: <code>{uploadId}</code></Text>}
          {uploadId && <a href={`/api/downloads/${uploadId}`}>Download</a>}
        </Box>
      )}
    </Box>
  )
}
