import React from 'react'
import { Flex, Box, Heading, Spacer, Button } from '@chakra-ui/react'

export default function Navbar() {
  return (
    <Flex as="header" align="center" padding={4} bg="gray.50" borderBottomWidth={1}>
      <Box>
        <Heading size="sm">LabFlow</Heading>
      </Box>
      <Spacer />
      <Box>
        <Button size="sm" variant="ghost">New Project</Button>
        <Button size="sm" variant="ghost" marginLeft={2}>Docs</Button>
      </Box>
    </Flex>
  )
}
