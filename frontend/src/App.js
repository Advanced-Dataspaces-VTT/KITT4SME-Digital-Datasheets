import React from 'react'
import { ReactKeycloakProvider } from '@react-keycloak/web'
import keycloak from './Keycloak'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import PrivateRoute from './helpers/PrivateRoute'

import HomePage from './pages/LandingPage'

import SearchResultSelectedPage from './pages/SearchResultSelected'
import CreateDataSheet from './pages/CreateDatasheetPage'
import SearchResults from './pages/SearchResults'

function App() {
  return (
    <div>
      <ReactKeycloakProvider
        initOptions={{
          onLoad: 'login-required',
          checkLoginIframe: false,
        }}
        authClient={keycloak}
      >
        <React.StrictMode>
          <BrowserRouter>
            <Routes>
              <Route
                path="*"
                element={
                  <PrivateRoute>
                    <HomePage />
                  </PrivateRoute>
                }
              />
              <Route
                path="/create-datasheet"
                element={
                  <PrivateRoute>
                    <CreateDataSheet />
                  </PrivateRoute>
                }
              />
              <Route
                path="/selected-search-result"
                element={
                  <PrivateRoute>
                    <SearchResultSelectedPage />
                  </PrivateRoute>
                }
              />
              <Route
                path="/search-results"
                element={
                  <PrivateRoute>
                    <SearchResults />
                  </PrivateRoute>
                }
              />
            </Routes>
          </BrowserRouter>
        </React.StrictMode>
      </ReactKeycloakProvider>
    </div>
  )
}

export default App
