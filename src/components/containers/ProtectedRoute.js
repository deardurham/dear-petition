import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect, Route } from 'react-router-dom';

import useAuth from '../../hooks/useAuth';
import { useLazyCheckLoginQuery } from '../../service/api';
import { loggedIn } from '../../slices/auth';

function ProtectedRoute({ children, ...props }) {
  const { user } = useAuth();
  const dispatch = useDispatch();
  const [checkLogin, { data, isFetching, isUninitialized }] = useLazyCheckLoginQuery();
  const isWaiting = isUninitialized || isFetching;

  useEffect(() => {
    if (!user && isUninitialized) {
      checkLogin();
    }
  }, [user, isUninitialized]);

  useEffect(() => {
    if (data?.user) {
      dispatch(loggedIn(data.user));
    }
  }, [data]);

  // Spin until user information provided or we are redirected
  // Note: extra render needed before loggedIn dispatch is propogated to useAuth()
  if (!user && (isWaiting || data?.user)) {
    return null;
  }

  return <Route {...props}>{user ? children : <Redirect to={{ pathname: '/login' }} />}</Route>;
}

export default ProtectedRoute;
