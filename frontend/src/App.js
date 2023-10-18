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
          onLoad: 'check-sso', // Change this to "check-sso"
          checkLoginIframe: false,
        }}
        authClient={keycloak}
      >
        <React.StrictMode>
          <BrowserRouter>
            <Routes>
              {/* Public route for HomePage */}
              <Route path="/" element={<HomePage />} />
              <Route path="/search-results" element={<SearchResults />} />
              <Route
                path="/selected-search-result"
                element={<SearchResultSelectedPage />}
              />

              {/* Private routes */}
              <Route
                path="*"
                element={
                  <PrivateRoute>
                    <Routes>
                      <Route
                        path="/create-datasheet"
                        element={<CreateDataSheet />}
                      />
                    </Routes>
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
