import React from 'react';
import { Route } from 'react-router-dom';

// Children
import LoginPage from '../pages/LoginPage/LoginPage';
import { USER } from '../../constants/authConstants';

function ProtectedRoute({ children, ...props }) {
  const user = localStorage.getItem(USER);

  if (!user) {
    return (
      <Route {...props}>
        <LoginPage redirect />
      </Route>
    );
  }
  return <Route {...props}>{children}</Route>;
}

export default ProtectedRoute;
