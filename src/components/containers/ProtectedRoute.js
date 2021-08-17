import React from 'react';
import { Redirect, Route } from 'react-router-dom';

// Children
import { USER } from '../../constants/authConstants';

function ProtectedRoute({ children, ...props }) {
  const user = localStorage.getItem(USER);

  return <Route {...props} render={() => (user ? children : <Redirect to="/login" />)} />;
}

export default ProtectedRoute;
