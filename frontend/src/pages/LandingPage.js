import React, { useState } from "react";
import axios from "axios";
import NavBar from "../components/NavBar.js";
import Footer from "../components/Footer";
import { Grid, FormControlLabel, FormGroup, Checkbox } from "@mui/material";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextInputComponent from "../components/TextInput.js";
import Spacer from "../components/Spacer";
import SingleButtonComponent from "../components/SingleButton.js";
import { useKeycloak } from "@react-keycloak/web";
import {useLocation, useNavigate} from "react-router-dom";

const HomePageFunctionality = () => {
  const [response, setResponse] = useState(null);
  const [filter, setFilter] = useState("");
  const [selectedCheckboxes, setselectedCheckboxes] = useState("")
  const [checkboxes, setCheckboxes] = useState({
    "module_properties.quality.issue_1": false,
    "module_properties.quality.issue_2": false,

    "module_properties.operator.issue_1": false,
    "module_properties.operator.issue_2": false,
    "module_properties.operator.issue_3": false,
    "module_properties.operator.issue_4": false,
    "module_properties.operator.issue_5": false,
    "module_properties.operator.issue_6": false,

    "module_properties.performance.issue_1": false,
    "module_properties.performance.issue_2": false,
    "module_properties.performance.issue_3": false,

    "module_properties.management.issue_1": false,
    "module_properties.management.issue_2": false,
    "module_properties.management.issue_3": false,

  });

  const { keycloak } = useKeycloak();
  const keycloak_id = keycloak.tokenParsed.sub;

  const handleCheckboxChange = (event) => {
    setCheckboxes({
      ...checkboxes,
      [event.target.value]: event.target.checked,
    });
  };

  const handleSearchClick = () => {
    const selectedCheckboxes = Object.entries(checkboxes)
      .filter(([, checked]) => checked)
      .map(([value]) => value);
    setselectedCheckboxes(selectedCheckboxes)
    const payload = {
      filter,
      selectedCheckboxes,
      keycloak_id,
    };
    console.log("PAYLOAD", payload);
    axios
      .post("http://kitt4sme.collab-cloud.eu/datasheets-backend-rest/datasheets-search", payload)
      .then((response) => {
        console.log(response.data);
        setResponse(response.data);
      })
      .catch((error) => console.error(error));
  };

  const handleResetClick = () => {
    setFilter("");
    setCheckboxes({
      "module_properties.quality.issue_1": false,
      "module_properties.quality.issue_2": false,

      "module_properties.operator.issue_1": false,
      "module_properties.operator.issue_2": false,
      "module_properties.operator.issue_3": false,
      "module_properties.operator.issue_4": false,
      "module_properties.operator.issue_5": false,
      "module_properties.operator.issue_6": false,

      "module_properties.performance.issue_1": false,
      "module_properties.performance.issue_2": false,
      "module_properties.performance.issue_3": false,

      "module_properties.management.issue_1": false,
      "module_properties.management.issue_2": false,
      "module_properties.management.issue_3": false,

    });
  };

  const navigate = useNavigate()
  const handleNavigation = () => {
    navigate('/search-results', {state: {'results': response.data}})
  }
  return (
    <>
      <div>
        <NavBar />
      </div>
      <div
        className="container-fluid"
        style={{ paddingTop: "5%", paddingBottom: "5%", width: "50%" }}
      >
        <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
          <Typography variant="h1" sx={{ width: "100%" }} gutterBottom>
            KITT4SME Digital Datasheets
          </Typography>
        </Box>
        <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
          <Typography variant="h2" sx={{ width: "100%" }} gutterBottom>
            SEARCH
          </Typography>
        </Box>
        <Spacer />
        <TextInputComponent
          sx={{ width: "100%" }}
          label={"Search text"}
          value={filter}
          handleChange={(e) => setFilter(e.target.value)}
        />
        <Spacer />
        <FormGroup>
          <Grid container direction="column" spacing={2}>
            <Grid item>
              <Grid container direction="row" spacing={2}>
                <Grid item xs={3}>
                  <Typography variant="h6">Quality</Typography>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.quality.issue_1"
                          checked={
                            checkboxes["module_properties.quality.issue_1"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Lack of automatic quality issue detection"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.quality.issue_2"
                          checked={
                            checkboxes["module_properties.quality.issue_2"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Inaccurate automatic quality inspection"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>

                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">Operator Wellbeing</Typography>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_1"
                          checked={
                            checkboxes["module_properties.operator.issue_1"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Preblematic interaction with automated elements"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_2"
                          checked={
                            checkboxes["module_properties.operator.issue_2"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ergonomics hazards in the workplace"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_3"
                          checked={
                            checkboxes["module_properties.operator.issue_3"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="High dependedence on operator experience and knowledge"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_4"
                          checked={
                            checkboxes["module_properties.operator.issue_4"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Production demand exceeding human capabilities"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_5"
                          checked={
                            checkboxes["module_properties.operator.issue_5"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Mentally demanding activities"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.operator.issue_6"
                          checked={
                            checkboxes["module_properties.operator.issue_6"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Limited operators knowledge or skills"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>

                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">Machine Performance</Typography>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.performance.issue_1"
                          checked={
                            checkboxes["module_properties.performance.issue_1"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Lack of predictive maintenance "
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.performance.issue_2"
                          checked={
                            checkboxes["module_properties.performance.issue_2"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ineffective set-up of parameters / tools "
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.performance.issue_3"
                          checked={
                            checkboxes["module_properties.performance.issue_3"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ineffective collection of performance data "
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>

                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h6">Production Management</Typography>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.management.issue_1"
                          checked={
                            checkboxes["module_properties.management.issue_1"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ineffective equipment production capacity management"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.management.issue_2"
                          checked={
                            checkboxes["module_properties.management.issue_2"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ineffective scheduling and resources allocation"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                  <Grid item>
                    <FormControlLabel
                      control={
                        <Checkbox
                          value="module_properties.management.issue_3"
                          checked={
                            checkboxes["module_properties.management.issue_3"]
                          }
                          onChange={handleCheckboxChange}
                          sx={{ fontSize: "1.5rem" }}
                        />
                      }
                      label="Ineffective analysis of performance data"
                      sx={{ fontSize: "1.5rem" }}
                    />
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </FormGroup>
        <Spacer />
        <Box display="flex" justifyContent="space-between" sx={{ gap: 2 }}>
          <SingleButtonComponent
            text={"Search"}
            path={""}
            handleClick={() => handleSearchClick()}
          />
          <SingleButtonComponent
            text={"Reset"}
            path={""}
            handleClick={() => handleResetClick()}
          />
        </Box>
        {response && response.data ? (
          <>
          <Typography sx={{ fontSize: "1.5rem" }} variant="h6">
            Search criteria yielded {response.data.length} results
          </Typography>
          <SingleButtonComponent
          text={"View results"}
          path={""}
          handleClick={() => handleNavigation()}
        />
        </>
        ) : null}
      </div>

      <div>
        <Footer />
      </div>
    </>
  );
};

function HomePage() {
  return <HomePageFunctionality />;
}

export default React.memo(HomePage);
