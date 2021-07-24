import { useEffect, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useLocation } from 'react-router-dom';

import { loggedIn } from '../slices/auth';
import { useCheckLoginMutation } from '../service/api';

const useAuth = () => {
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const [checkLogin] = useCheckLoginMutation();
  const history = useHistory();
  const location = useLocation();
  const { pathname } = location || { pathname: '/' };

  useEffect(() => {
    if (!user) {
      checkLogin()
        .unwrap()
        .then((data) => {
          dispatch(loggedIn(data.user));
          history.replace(pathname);
        });
    }
  }, [user]);
  return useMemo(() => ({ user }), [user]);
};

export default useAuth;
