import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import useAuth from '../../hooks/useAuth';

function ProtectedRoute({ children, ...props }) {
  const { user } = useAuth();
  return <Route {...props} render={() => (user ? children : <Redirect to="/login" />)} />;
}

export default ProtectedRoute;
