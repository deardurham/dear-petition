import React from 'react';
import { Route } from 'react-router';

// Children
import LoginPage from '../pages/LoginPage/LoginPage';


function ProtectedRoute({ children, ...props }) {
    // TODO: When implementing auth, set this to some localStorage doo.
    const authorized = localStorage.getItem('AUTHORIZED') === 'true';

    if (!authorized) return <Route {...props}><LoginPage redirect /></Route>
    return <Route {...props}>{children}</Route>
}

export default ProtectedRoute;
