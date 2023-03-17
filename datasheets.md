# High-level functionality
Digital datasheet enable coherent information to be collected from AI modules. Datasheets are accompanied with tool for filling out and formatting the data sheets to user friendly format that enables component manufacturers to fill and submit datasheet information in the RAMP tool.
# Role in the architecture
Digital datasheet tool is related to Discovery and Composition slots in the Kitt4SME user journey. Datasheets gather information about the components and formats in useable form for adaptive questionnaire and other parts of the Kitt4SME platform that can benefit from the information
Digital datasheet tool is used through RAMP marketplace and provides platform level functionality for other components to use
# Requirements  
There are requirements for digital data sheets and tools related to the datasheets:
- Collect information from the component related to ciritical questions in Adaptive Questionnaire
- Collect information related to deployment of the components
- - component hardware dependencies
- - component software dependencies
- Describe API exposed by the compoent if any
- Describe datamodel that component uses
- RAMP integratable tool for composing the datasheet and store it in the marketplace
- - Should be able to edit information in the RAMP marketplace
- - Should be anable format datasheet in user friendly format
# Improvements
Improvement that the datasheet tool brings is that it enables automated linking of component information to the adaptive questionnaire so that relevant components can easily retrieved. 
Since datasheet also collects information about the deployment and integration of the tool it helps the evaluation and deployment of the AI component.
Data sheet tool to fill out the information in easy and informative way is new development and talor made based on knowledge collected in Kitt4SME project
# Value proposition
Two major benefits tha digital datasheets bring in the project are:
- AI specific information model of software components enabling automated linking of components with user requirements
- Information of compoent deployment in coherent way which enables to compare compoents against dependencies and requirements.
# Deployment
Digital datasheets are are stored in RAMP marketplace database and accessible thru RAMP marketplace
Datasheet tool is integrated into RAMP marketplace as micro service. Tool is implemented as Node.js application
and distributed as docker container. Security of the component is done via RAMP marketplace since the tool is running in the scope of RAMP marketplace
