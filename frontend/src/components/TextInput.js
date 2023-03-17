import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';



export default function TextInputComponent(props) {

  return (
    <Box sx={{'& .MuiTextField-root': { width: '100%'}}}>   
    <TextField
      id="outlined-multiline-static"
      label={props.label}
      InputProps={{ style: { fontSize: '1.5rem' } }}
      InputLabelProps={{ style: { fontSize: '1.5rem' }, shrink: true }}
      onChange={props.handleChange}
      disabled={props.disabled}
      value={props.value}
    />
  </Box>
  );
}