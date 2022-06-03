import { useMemo } from 'react';
import { useSelector } from 'react-redux';

const useAuth = () => {
  const user = useSelector((state) => state.auth.user);
  return useMemo(() => ({ user }), [user]);
};

export const useIsAdmin = () => {
  const { user } = useAuth();
  return user?.is_admin;
};

export default useAuth;
