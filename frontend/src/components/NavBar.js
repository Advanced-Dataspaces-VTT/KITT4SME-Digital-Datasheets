import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

import ProfileIcon from '../components/ProfileIcon'
import {useNavigate} from "react-router-dom";

export default function ButtonAppBar(props) {

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar style={{background: "#60c4dc"}}>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontSize: 20 }}>
            KITT4SME DIGITAL DATASHEETS
          </Typography>
          {
            props.secure == false ? null : <ProfileIcon/>
          }
          
        </Toolbar>
      </AppBar>
    </Box>
  );
}