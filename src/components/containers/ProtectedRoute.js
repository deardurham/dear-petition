import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Route, Redirect } from 'react-router-dom';

import useAuth from '../../hooks/useAuth';
import { useCheckLoginMutation } from '../../service/api';
import { loggedIn } from '../../slices/auth';

function ProtectedRoute({ children, ...props }) {
  const { user } = useAuth();
  const [checkLogin, { isLoading, isSuccess, isUninitialized }] = useCheckLoginMutation();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!user && isUninitialized) {
      checkLogin()
        .unwrap()
        .then((data) => {
          dispatch(loggedIn(data.user));
        });
    }
  }, [user, isUninitialized]);

  // make decision to redirect after checking login information
  // note: don't redirect on success because it's handled in useEffect
  if (!user && (isUninitialized || isLoading || isSuccess)) {
    return null;
  }

  return (
    <Route {...props} render={() => (user ? children : <Redirect to={{ pathname: '/login' }} />)} />
  );
}

export default ProtectedRoute;
