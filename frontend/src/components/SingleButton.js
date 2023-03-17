import * as React from 'react';
import Button from '@mui/material/Button';

export default function SingleButtonComponent(props) {
    return (
        <Button 
            variant={props.variant}
            sx={{ width: "100%", background: "#60c4dc", color: "white", "&:hover":{ backgroundColor: "#31b0d6"} }}
            style={{ fontSize: '2rem', textTransform: 'none'}}
            onClick={props.handleClick}
            onSubmit={props.handleSubmit}
            >
                {props.text}
            </Button>
    );
}