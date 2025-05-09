// src/pages/Home.jsx
import React, { useState } from 'react';
import UploadEmail from '../components/UploadEmail';
import PredictionResult from '../components/PredictionResult';
import { Box, Heading } from '@chakra-ui/react';

const Home = () => {
  const [result, setResult] = useState(null);

  return (
    <Box p={8}>
      <Heading mb={6}>Asthra MailGuard – Smart Email Classifier</Heading>
      <UploadEmail setResult={setResult} />
      <PredictionResult result={result} />
    </Box>
  );
};

export default Home;
