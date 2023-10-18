import React, { memo, useState } from 'react'

import Button from '@mui/material/Button'
import Snackbar from '@mui/material/Snackbar'
import IconButton from '@mui/material/IconButton'
import CloseIcon from '@mui/icons-material/Close'

import applyRules from 'rjsf-conditionals'
import Engine from 'json-rules-engine-simplified'
import Form from '@rjsf/core'
//import schema from './form/schema.json';
import schema from '../static/content.json'
import uiSchema from './form/uiSchema.json'
import rules from './form/rules.json'
import Footer from '../components/Footer'
import NavBar from '../components/NavBar'
import keycloak from '../Keycloak'
import SingleButton from '../components/SingleButton'
import Spacer from '../components/Spacer'
import Stack from '@mui/material/Stack'
import TextInput from '../components/TextInput'
import { useLocation, useNavigate } from 'react-router-dom'

import { CREATE_DATASHEET_URL } from '../util/urls.js'

const onSubmit = async ({ formData }) => {
  try {
    const response_keycloak = await keycloak.loadUserInfo()
    formData['keycloak_id'] = response_keycloak.sub
    const url = CREATE_DATASHEET_URL
    const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(formData),
    })
    if (response.status === 200) {
      alert('Success: Datasheet created successfully.')
    } else {
      alert('Error: Datasheet was not created successfully.')
    }
  } catch (err) {
    alert('Error: Unknown error has occurred!')
  }
}

const exportData = async ({ formData }) => {
  const jsonString = `data:text/json;chatset=utf-8,${encodeURIComponent(
    formData,
  )}`
  const link = document.createElement('a')
  link.href = jsonString
  link.download = 'data.json'
  link.click()
}

const extraActions = {
  log: (params, schema, uiSchema, formData) => {
    //console.log(params, schema, uiSchema, formData);
    //console.log(formData['information']);
  },
}

const FormWithConditionals = applyRules(
  schema,
  uiSchema,
  rules,
  Engine,
  extraActions,
)(Form)

const UploadFunctionality = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const hiddenFileInput = React.useRef(null)
  let uploadedData = null

  if (location.state) {
    uploadedData = location.state.data['datasheet']
  }

  const handleNavigation = (path, data) => {
    navigate(path, { state: { data: data } })
  }

  const handleFileChange = (event) => {
    event.preventDefault()
    const reader = new FileReader()
    if (event.target.files[0]) {
      if (event.target.files[0].type === 'application/json') {
        const fileUploaded = event.target.files[0]
        reader.onload = (event) => {
          const { result } = event.target
          handleInputText(result)
        }
        reader.readAsText(fileUploaded)
      }
      hiddenFileInput.current.value = null
    }
  }

  const handleInputText = (value) => {
    let json = JSON.parse(value)
    handleNavigation('/create-datasheet', json)
  }

  const handleFilePicker = () => {
    hiddenFileInput.current.click()
  }

  return (
    <>
      <div>
        <NavBar />
      </div>

      <div
        className="container-fluid"
        style={{ paddingTop: '5%', paddingBottom: '5%', width: '50%' }}
      >
        {/*<Stack spacing={2} direction="column">
          <>
            <SingleButton
              text={'Upload datasheet'}
              path={''}
              handleClick={() => handleFilePicker()}
            />
            <input
              type="file"
              accept="application/json"
              ref={hiddenFileInput}
              onChange={(e) => handleFileChange(e)}
              style={{ display: 'none' }}
            />
          </>
        </Stack>*/}

        <Spacer />

        <FormWithConditionals
          showErrorList={true}
          onSubmit={onSubmit}
          formData={uploadedData}
          uiSchema={uiSchema}
        ></FormWithConditionals>
      </div>
      <div>
        <Footer />
      </div>
    </>
  )
}

function CreateDatasheetPage() {
  return <UploadFunctionality />
}

export default React.memo(CreateDatasheetPage)
