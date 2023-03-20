import React from "react";
import {ReactKeycloakProvider} from "@react-keycloak/web";
import keycloak from "./Keycloak";
import {BrowserRouter, Route, Routes} from "react-router-dom";

import PrivateRoute from "./helpers/PrivateRoute";

import HomePage from "./pages/LandingPage";

import SearchResultSelectedPage from "./pages/SearchResultSelected"
import CreateDataSheet from "./pages/CreateDatasheetPage";

function App() {
    return (
        <div>
            <ReactKeycloakProvider
                initOptions={{
                  onLoad: "login-required",
                  checkLoginIframe: false,
                }}
                authClient={keycloak}>
                <React.StrictMode>
                    <BrowserRouter>
                        <Routes>
                            <Route
                                path="*"
                                element={
                                    <PrivateRoute>
                                        <HomePage/>
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/create-datasheet"
                                element={
                                    <PrivateRoute>
                                        <CreateDataSheet/>
                                    </PrivateRoute>
                                }
                            />
                            <Route
                                path="/selected-search-result"
                                element={
                                    <PrivateRoute>
                                        <SearchResultSelectedPage/>
                                    </PrivateRoute>
                                }
                            />
                        </Routes>
                    </BrowserRouter>
                </React.StrictMode>
            </ReactKeycloakProvider>
        </div>
    );
}

export default App;