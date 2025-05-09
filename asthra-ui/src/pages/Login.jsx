// src/pages/Login.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Button, Heading, VStack, Text, useToast
} from '@chakra-ui/react';
import { auth, signInWithGoogle } from '../firebase/auth';

const Login = () => {
  const navigate = useNavigate();
  const toast = useToast();

  const handleGoogleLogin = async () => {
    try {
      await signInWithGoogle();
      toast({ title: 'Logged in successfully!', status: 'success' });
      navigate('/');
    } catch (err) {
      toast({ title: err.message, status: 'error' });
    }
  };

  useEffect(() => {
    // If already logged in, redirect to Home
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) navigate('/');
    });
    return () => unsubscribe();
  }, [navigate]);

  return (
    <Box p={8}>
      <VStack spacing={6}>
        <Heading>Welcome to Asthra MailGuard</Heading>
        <Text>Sign in with your Google Account</Text>
        <Button colorScheme="red" onClick={handleGoogleLogin}>
          Sign in with Google
        </Button>
      </VStack>
    </Box>
  );
};

export default Login;
