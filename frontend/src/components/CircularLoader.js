import React, {useState} from "react";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

export default function CircularLoaderComponent() {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center'}}>
            <CircularProgress />
        </Box>
    )
}