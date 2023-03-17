import React, {useState} from "react";
import Title from "../components/Title.js"
import NavBar from "../components/NavBar.js"
import CardComponent from "../components/CardComponent.js"
import {useLocation, useNavigate} from "react-router-dom";
import Footer from "../components/Footer";
import Spacer from "../components/Spacer"
import Paper from '@mui/material/Paper';
import CircularLoaderComponent from "../components/CircularLoader";

const SearchResultsPageFunctionality = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const [results, setResults] = useState(location?.state?.results);
    const [loading, setLoading] = useState(false);
    const [searchResults, setSearchResults] = useState([])

    const handleNavigation = (clickedItemData) => {
        navigate("/selected-search-result", {state: {'data': clickedItemData}})
    }

    const handleClick = (clickedItemData) => {
        handleNavigation(clickedItemData)
    }
    return (
        <>

            <div>
                <NavBar/>
            </div>
            <div className="container-fluid" style={{paddingTop: "5%", paddingBottom: "5%", width: "50%"}}>

                {
                    results != undefined ?
                    <>
                <Spacer/>
                {
                    loading ?
                        <>
                            <Title text={"Loading datasheets"}/>
                            <Spacer/>
                            <CircularLoaderComponent/>
                        </>
                        :
                        <>
                            <Spacer/>
                            <Paper style={{maxHeight: 500, maxWidth: 1500, overflow: 'auto'}}>
                                {
                                    Object.keys(results).map((key, index) => {
                                        {console.log(" results ", results[0])}
                                        return (
                                            <div key={key}>
                                                <Spacer/>
                                                <CardComponent
                                                    component_name={results[index].datasheet?.information?.component_name}
                                                    description={results[index].datasheet?.information?.description}
                                                    provider={results[index].datasheet?.information?.provider}
                                                    version={results[index].datasheet?.information?.version}
                                                    handleClick={() => handleClick(results[index])}
                                                />
                                            </div>
                                        )
                                    })
                                }
                            </Paper>
                            <Spacer/>
                            <Title text={"Loaded: " +  Object.keys(results).length + " datasheets"}/>
                        </>


                }</>
                : <>
                <Title text={"Error loading datasheets "}/>
                <Spacer/>
            </>}

                <Spacer/>

            </div>

            <div>
                <Footer/>
            </div>
        </>
    )
}

function SearchResultsPage() {
    return <SearchResultsPageFunctionality/>
}

export default React.memo(SearchResultsPage)