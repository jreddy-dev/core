import React from 'react'
import VideoUploader from './components/VideoUploader'
import Flowchart from './components/Flowchart'
import ExperimentView from './components/ExperimentView'
import ProtocolReview from './components/ProtocolReview'
import Navbar from './components/Navbar'
import { Box, Flex } from '@chakra-ui/react'

export default function App() {
  return (
    <Box minH="100vh">
      <Navbar />
      <Flex padding={6} gap={6}>
        <Box flex="1" borderWidth={1} borderRadius="md" padding={4} bg="white">
          <Flowchart />
        </Box>
        <Box width="420px" borderWidth={1} borderRadius="md" padding={4} bg="white">
          <VideoUploader />
          <ExperimentView />
          <ProtocolReview />
        </Box>
      </Flex>
    </Box>
  )
}
