import * as React from 'react'
import Button from '@mui/material/Button'

export default function SingleButtonComponent(props) {
  return (
    <Button
      variant={props.variant}
      sx={{
        width: '100%',
        background: 'red', // Change this line to set the background to red
        color: 'white',
        '&:hover': { backgroundColor: 'red' },
      }}
      style={{ fontSize: '2rem', textTransform: 'none' }}
      onClick={props.handleClick}
      onSubmit={props.handleSubmit}
    >
      {props.text}
    </Button>
  )
}
