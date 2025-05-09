import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
  const { authUser, loading } = useAuth();

  if (loading) return <p>Loading...</p>;

  return authUser ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
