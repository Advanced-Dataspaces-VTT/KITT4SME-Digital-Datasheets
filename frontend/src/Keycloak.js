import Keycloak from "keycloak-js";
import config from "./config.json";

const keycloak = new Keycloak({
    url: config["KEYCLOAK_URL"],
    realm: config["KEYCLOAK_REALM"],
    clientId: config["KEYCLOAK_CLIENT_ID"]
});

export default keycloak;