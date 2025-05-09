// src/components/PredictionResult.jsx
import React from 'react';
import { Box, Badge, Text, VStack, Heading } from '@chakra-ui/react';

const PredictionResult = ({ result }) => {
  if (!result) return null;

  return (
    <Box p={6} borderWidth={1} borderRadius="lg" mt={4}>
      <Heading size="md" mb={2}>Prediction Result</Heading>
      <VStack align="start" spacing={2}>
        <Text><strong>Label:</strong> <Badge colorScheme="green">{result.label}</Badge></Text>
        <Text><strong>Confidence:</strong> {Math.round(result.confidence * 100)}%</Text>
        <Text><strong>Method:</strong> {result.method}</Text>
      </VStack>
    </Box>
  );
};

export default PredictionResult;
