import { useKeycloak } from "@react-keycloak/web";

const PrivateRoute = ({ children }) => {
    const { keycloak } = useKeycloak();
    const isLoggedIn = keycloak.authenticated;
    if (isLoggedIn) {
        return children
    }
    return null;
};

export default PrivateRoute;