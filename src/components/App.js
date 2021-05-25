import React from 'react';
import { AppStyled } from './App.styled';
import GlobalStyle from '../styles/GlobalStyle';
import { Provider as AlertProvider } from 'react-alert';

// Routing
import { BrowserRouter, Switch } from 'react-router-dom';
import ProtectedRoute from './containers/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage/HomePage';
import GenerationPage from './pages/GenerationPage/GenerationPage';
import FAQPage from './pages/HelpPage/HelpPage';
import Alert from './elements/Alert/Alert';

const alertOptions = {
  position: 'bottom right',
  timeout: 5000,
  transition: 'scale'
};

function App() {
  return (
    <>
      <GlobalStyle />
      <BrowserRouter>
        <AlertProvider template={Alert} {...alertOptions}>
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
        </AlertProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
