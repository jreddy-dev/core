import React, { useState } from 'react'

export default function VideoUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)

  async function upload() {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    // Using a demo experiment id
    const res = await fetch('/api/videos/demo-experiment', {
      method: 'POST',
      body: form
    })
    if (res.ok) {
      const j = await res.json()
      setStatus(JSON.stringify(j))
    } else {
      setStatus('Upload failed')
    }
  }

  return (
    <div>
      <input type="file" accept="video/*" onChange={e => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={upload} disabled={!file} style={{ marginLeft: 8 }}>
        Upload
      </button>
      {status && <pre>{status}</pre>}
    </div>
  )
}
