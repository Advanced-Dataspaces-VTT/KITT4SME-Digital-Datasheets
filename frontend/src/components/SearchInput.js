import * as React from 'react';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';


export default function InputAdornments(props) {
  const [values, setValues] = React.useState({
    username: '',
  });

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
  };

  return (
    <Box 
        sx={{ display: 'flex', flexWrap: 'wrap', }}>
        <FormControl sx={{width: 500, alignContent: 'flex-end' , fontSize: '1.5rem' }} variant="outlined">
          <InputLabel 
            htmlFor="outlined-adornment-username"
            sx={{fontSize: '1.5rem' }}
            >
                {props.text}
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-username"
            type={'text'}
            value={values.username}
            onChange={handleChange('username')}
            label="Password"
            sx={{fontSize: '1.5rem' }}
          />
        </FormControl>
    </Box>
  );
}