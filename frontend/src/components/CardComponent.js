import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


export default function BasicCard(props) {
    return (
        <Card sx={{m: 1, minWidth: 275}}>
            <CardContent>
                <Typography sx={{fontSize: 14}} color="text.secondary" gutterBottom>
                    Component name: <br /> {props.component_name}
                </Typography>
                <Typography variant="h5" component="div" sx={{fontSize: 14}}>
                    Version: <br /> {props.version}
                </Typography>
                <Typography sx={{mb: 1.5, fontSize: 14}} color="text.secondary">
                    Provider: <br /> {props.provider}
                </Typography>
                <Typography variant="body2" sx={{fontSize: 14}}>
                    Description: <br /> {props.description}
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="large" sx={{fontSize: 14}} onClick={props.handleClick}>View</Button>
            </CardActions>
        </Card>
    );
}


