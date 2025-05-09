// src/components/UploadEmail.jsx
import React, { useState } from 'react';
import { Box, Textarea, Button, Heading, useToast } from '@chakra-ui/react';
import axios from 'axios';

const UploadEmail = ({ setResult }) => {
  const [emailText, setEmailText] = useState('');
  const [sender, setSender] = useState('');
  const toast = useToast();

  const handleClassify = async () => {
    if (!sender || !emailText) {
      toast({ title: 'Sender and content required', status: 'warning' });
      return;
    }

    try {
      const res = await axios.post('http://localhost:8000/predict-email', {
        sender,
        text: emailText
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      toast({ title: 'Error classifying email', status: 'error' });
    }
  };

  return (
    <Box p={6}>
      <Heading size="md" mb={4}>Paste Email Content</Heading>
      <Textarea
        placeholder="Sender email (e.g. hr@naukri.com)"
        mb={2}
        value={sender}
        onChange={(e) => setSender(e.target.value)}
      />
      <Textarea
        placeholder="Paste the email text here..."
        rows={8}
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
      />
      <Button mt={4} colorScheme="blue" onClick={handleClassify}>Classify</Button>
    </Box>
  );
};

export default UploadEmail;
