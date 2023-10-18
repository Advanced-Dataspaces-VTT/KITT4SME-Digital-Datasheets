import React, { useState, useEffect } from "react";
import axios from "axios";
import NavBar from "../components/NavBar.js";
import Footer from "../components/Footer";
import { useLocation, useNavigate } from "react-router-dom";

import Title from "../components/Title.js";
import CardComponent from "../components/CardComponent.js";
import Paper from "@mui/material/Paper";
import CircularLoaderComponent from "../components/CircularLoader";
import Spacer from "../components/Spacer";


const SearchResultsFunctionality = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [response, setResponse] = useState(location.state?.results || null);
  const handleNavigationClick = (clickedItemData) => {
    navigate("/selected-search-result", { state: { data: clickedItemData } });
  };

  const handleClick = (clickedItemData) => {
    console.log("Click", clickedItemData)
    handleNavigationClick(clickedItemData);
  };
  return (
    <>
      <div>
        <NavBar />
      </div>
      <div className="container-fluid" style={{ paddingBottom: "5%", width: "50%" }}>
        <div className="container-fluid" style={{ paddingTop: "5%", paddingBottom: "5%", width: "100%" }}>
        {response && Array.isArray(response) && response.length > 0 ? (
  <>
  { console.log(" response.data ", response) } 
    <Spacer />
    <Title text="Search results" />
    <Spacer />
    <Paper style={{ maxHeight: 500, maxWidth: 1500, overflow: "auto" }}>
      {response && Object.keys(response).map((key, index) => {
        
        return (
          <div key={key}>
            <Spacer />
            <CardComponent
              component_name={response[index]?.datasheet?.information?.component_name}
              description={response[index]?.datasheet?.information?.description}
              provider={response[index]?.datasheet?.information?.provider}
              version={response[index]?.datasheet?.information?.version}
              handleClick={() => handleClick(response[index])}
            />
          </div>
        );
      })}
    </Paper>
    <Spacer />
  </>
) : (
  <>
    <Title text="Error loading the results" />
  </>
)}

        </div>
      </div>
      <div>
        <Footer />
      </div>
    </>
  );
};

function SearchResultsPage() {
  return <SearchResultsFunctionality />;
}

export default React.memo(SearchResultsPage);
