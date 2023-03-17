import * as React from 'react';
import { useNavigate } from "react-router-dom"
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';

import { useKeycloak } from "@react-keycloak/web";

export default function ProfileIconComponent() {
    const navigate = useNavigate()

    const { keycloak } = useKeycloak();

    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleNavigation = (path) => {
        navigate(path)
        handleClose()
    }

    return(
        <>
            <IconButton
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
            >
            <AccountCircle sx={{ fontSize: "30px" }}  />
            </IconButton>
                <Menu
                     sx={{ mt: '50px' }}
                     id="menu-appbar"
                     anchorEl={anchorEl}
                     anchorOrigin={{
                       vertical: 'top',
                       horizontal: 'right',
                     }}
                     keepMounted
                     transformOrigin={{
                       vertical: 'top',
                       horizontal: 'right',
                     }}
                     open={Boolean(anchorEl)}
                     onClose={handleClose}
                >
                    {/*<MenuItem onClick={() => handleNavigation('/my-profile')} sx={{fontSize: 15}}>My profile</MenuItem>
                    <MenuItem onClick={() => handleNavigation('/my-datasheets')} sx={{fontSize: 15}}>My datasheets</MenuItem>
                    <MenuItem onClick={() => handleNavigation('/create-datasheet')} sx={{fontSize: 15}}>Create datasheet</MenuItem>
                    <MenuItem onClick={() => handleNavigation('/Search')} sx={{fontSize: 15}}>Search</MenuItem>*/}
                    <MenuItem onClick={() => handleNavigation('/Search')} sx={{fontSize: 15}}>Search</MenuItem>
                    <MenuItem onClick={() => handleNavigation('/create-datasheet')} sx={{fontSize: 15}}>Create datasheet</MenuItem>
                    <MenuItem onClick={() => keycloak.logout()} sx={{fontSize: 15}}>Logout</MenuItem>
            </Menu>
        </>
    )
}