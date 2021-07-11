import React from 'react';
import AppStyled from './App.styled';
import GlobalStyle from '../styles/GlobalStyle';

// Routing
import { BrowserRouter, Switch } from 'react-router-dom';
import ProtectedRoute from './containers/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage/HomePage';
import GenerationPage from './pages/GenerationPage/GenerationPage';
import FAQPage from './pages/HelpPage/HelpPage';

function App() {
  return (
    <>
      <GlobalStyle />
      <BrowserRouter>
        <AppStyled>
          <Switch>
            <ProtectedRoute exact path="/">
              <HomePage />
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
