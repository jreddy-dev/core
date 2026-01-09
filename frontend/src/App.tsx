import React from 'react'
import VideoUploader from './components/VideoUploader'
import Flowchart from './components/Flowchart'
import ExperimentView from './components/ExperimentView'
import ProtocolReview from './components/ProtocolReview'

export default function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>LabFlow Prototype</h1>
      <div style={{ display: 'flex', gap: 20 }}>
        <div style={{ flex: 1 }}>
          <Flowchart />
        </div>
        <div style={{ width: 360 }}>
          <VideoUploader />
          <ExperimentView />
          <ProtocolReview />
        </div>
      </div>
    </div>
  )
}
