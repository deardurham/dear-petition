import React, { useEffect } from 'react';
import styled from 'styled-components';
import AppStyled from './App.styled';
import GlobalStyle from '../styles/GlobalStyle';

// Routing
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ProtectedRoute from './containers/ProtectedRoute';

import { Button } from './elements/Button';
import Modal from './elements/Modal/Modal';
import HomePage from './pages/HomePage/HomePage';
import GenerationPage from './pages/GenerationPage/GenerationPage';
import FAQPage from './pages/HelpPage/HelpPage';
import LoginPage from './pages/LoginPage/LoginPage';
import { CSRF_TOKEN_LS_KEY, USER } from '../constants/authConstants';
import useBrowserWarning from '../hooks/useBrowserWarning';
import UsersPage from './pages/UsersPage/UsersPage';
import AgenciesPage from './pages/AgenciesPage';

const WarningModal = styled(Modal)`
  width: 500px;

  & > div {
    gap: 1rem;
    padding: 2rem;
    & > h3 {
      font-weight: 700;
      align-self: center;
    }
    & > button {
      margin-top: 1rem;
      align-self: center;
      width: 100px;
    }
  }
`;

const BrowserWarning = ({ hideModal, showWarning }) => (
  <WarningModal isVisible={showWarning} closeModal={hideModal}>
    <h3>WARNING</h3>
    <p>It appears you are not using Chrome. This may cause issues while using the application.</p>
    <p>Please use Chrome to ensure best results.</p>
    <Button onClick={hideModal}>Close</Button>
  </WarningModal>
);

function App() {
  const [showWarning, hideModal] = useBrowserWarning();
  useEffect(() => {
    // avoid local storage now we're using redux and properly using cookies
    if (localStorage.getItem(CSRF_TOKEN_LS_KEY)) {
      localStorage.removeItem(CSRF_TOKEN_LS_KEY);
    }
    if (localStorage.getItem(USER)) {
      localStorage.removeItem(USER);
    }
  }, []);

  return (
    <>
      <GlobalStyle />
      <BrowserRouter>
        <AppStyled>
          <Switch>
            <Route path="/login">
              <>
                <LoginPage />
                <BrowserWarning showWarning={showWarning} hideModal={hideModal} />
              </>
            </Route>
            <ProtectedRoute exact path="/">
              <>
                <HomePage />
                <BrowserWarning showWarning={showWarning} hideModal={hideModal} />
              </>
            </ProtectedRoute>
            <ProtectedRoute exact path="/generate/:batchId">
              <GenerationPage />
            </ProtectedRoute>
            <ProtectedRoute exact path="/users" isAdminOnly>
              <UsersPage />
            </ProtectedRoute>
            <ProtectedRoute exact path="/agencies" isAdminOnly>
              <AgenciesPage />
            </ProtectedRoute>
            <ProtectedRoute exact path="/help">
              <FAQPage />
            </ProtectedRoute>
          </Switch>
        </AppStyled>
      </BrowserRouter>
    </>
  );
}

export default App;
