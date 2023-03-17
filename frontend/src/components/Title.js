import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

export default function TitleC(props) {
    return (
        <Box sx={{ width: '100%', maxWidth: 500 }}>
            <Typography variant="h4" gutterBottom>
                {props.text}
            </Typography>
        </Box>
    );
}