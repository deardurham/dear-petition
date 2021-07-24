import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import useAuth from '../../hooks/useAuth';

function ProtectedRoute({ children, ...props }) {
  const { user } = useAuth();
  return (
    <Route
      {...props}
      render={({ location }) =>
        user ? children : <Redirect to={{ pathname: '/login', state: { from: location } }} />
      }
    />
  );
}

export default ProtectedRoute;
