import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function SearchResult(props) {
    return (
        <Box sx={{ p: 4, borderRadius: 1, p: 4, border: '1px solid'}} style={{ width:"100%" }}>
            <Typography variant='body' style={{ width:"100%", textAlign: "left" }}>
                {props.text}
            </Typography>
            <Button variant="contained" style={{ float:"right"}}>{props.owned}</Button>
        </Box>
    );
}