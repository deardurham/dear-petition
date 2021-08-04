import React from 'react';
import AppStyled from './App.styled';
import GlobalStyle from '../styles/GlobalStyle';

// Routing
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import ProtectedRoute from './containers/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage/HomePage';
import GenerationPage from './pages/GenerationPage/GenerationPage';
import FAQPage from './pages/HelpPage/HelpPage';
import LoginPage from './pages/LoginPage/LoginPage';
import useBrowserWarning from '../hooks/useBrowserWarning';
import { ModalStyled, ModalContent } from './pages/HomePage/HomePage.styled';

const BrowserWarning = ({ hideModal, showWarning }) => (
  <ModalStyled isVisible={showWarning} closeModal={hideModal}>
    <ModalContent>
      <h3>WARNING</h3>
      <p>
        It appears you are not using Chrome. Non-Chrome browsers are not supported for this
        application. Please use Chrome to ensure best results.
      </p>
    </ModalContent>
  </ModalStyled>
);

function App() {
  const [showWarning, hideModal] = useBrowserWarning();
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
