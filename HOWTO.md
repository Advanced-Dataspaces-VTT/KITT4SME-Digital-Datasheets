# Introduction

# Login to the tool
There is two ways to login to the Datasheet tool: By using your RAMP.eu credentials (1), or by registering solely for the datasheet tool (1). RAMP credentials you can obtain by registering at ramp.eu. 
![Alt text](docs/sc1.png?raw=true "Login to the the tool")
Once log in the tool you can search, view and create datasheets for your AI component.
# Creating Datasheet
You can create datasheets by clicking "Create datasheet" -link from the menu that is at the top right corner of the screen (3).´
![Alt text](docs/sc2.png?raw=true "Create Datasheets")
Create datasheet takes you to the form which contains fields for the information required for the component. 

## Registration data 
This section collects identification information of the AI component which will be used for its tracking in RAMP.
### Component name
(Open-ended)
Mandatory	Fill in by providing the full name of the component. 

The name can contain capital letters, numbers, and special characters. The text to be inserted must be bound by a minimum and maximum number of characters.
### Component Acronym
(Open-ended)
Mandatory	Fill in by providing the short name of the component. 

The acronym can contain capital letters, numbers, and special characters. The text to be inserted must be bound by a minimum and maximum number of characters.
### Component UUID
(Open-ended)
Mandatory	Fill by providing the component UUID hash.

The component UUID is a sequence of hexadecimal characters representing a fixed-length numerical value, therefore this field can contain an alphanumeric text.
### Provider
(Open-ended)
Not mandatory	Fill in by providing the link to the component provider information.
### Version
(Open-ended)
Mandatory	Fill in by providing the latest version number of the component. 

The version can contain capital letters, numbers, and special characters. The text to be inserted must be bound by a minimum and maximum number of characters.
##	Component Description 
The second section is dedicated to the functional description of the AI component. The information requested are essential not only for labelling, organizing and tracking the component but also for gaining awareness and knowledge of its characteristics at a business level.
###	Applicable industries
(Multiple choice) 
Mandatory	Tick the industrial manufacturing sectors that best characterize the field of operability of the component. The list provided derives from the codes of NACE system codes.

###	Axis
(Multiple choice)
Mandatory	Tick the axis/s to which the component belongs. The component should troubleshoot, and address challenges related to one or more of the KITT4SME axes:
□	AI for human-robot interaction: acts by providing the means for real-time monitoring of the psychological and physical conditions of workers, activation of fatigue and stress-relieving interventions as well as for the characterization and evolution of workforce competences.
□	AI for quality: acts by providing the means for early and automatic error-detection and better run time decisions. A quality issue results in reworking costs, customer assistance costs or even recalls of entire production lots depending on how fast it is detected.
□	AI for reconfigurability or product personalization addresses the complexity of production processes that are increasingly influenced by product customization. It moves beyond standard linear optimization-based approaches that focus on raw material availability, production capacity and demand, working at both the optimization of production settings and scheduling and planning levels.
###	Category
(Multiple choice)
Mandatory	Tick the type of component among the two macro-categories:
□	Reasoning Engine: reasoning engine module reads the data streams, merge them and detect possible deviations from desired effects. This kind of module can be dedicated to detecting heterogeneous conditions such as divergence of machine or process parameters, fluctuations in quality, vibrations, physical or mental stress of operators among many others.
□	Decision making: decision maker module generates in real-time interventions to be applied in the shop floor. Scope and underlying technologies can vary broadly, depending on the observed problem: optimisation algorithms cope with flexible production demands finding the trade-off between conflicting objectives, models for time-series analysis find patterns in monitored parameters to predict upcoming quality issues, rule-based modules orchestrate the human-machine interactions by suggesting relieving actions when operators become fatigued or stressed; intrinsic job rotation in which cobots change their behaviour to break the routine of repetitive tasks is proposed by machine learning modules.
###	Description
(Open-ended)
Mandatory	Fill in by providing a brief and general description of how the functional characteristics of the component work to provide the expected result.

The text to be inserted must be bound by a minimum and maximum number of characters. 
###	Features
(Multiple choice)
Mandatory	Tick the main features that provide information about the capabilities of the component. They are reflected in 4 categories in line with the main dynamics where the major production critical issues are present: Quality, Operator Wellbeing, Machine Performance and Production Management.

It is mandatory to provide at least one feature regardless of the category. Features can also be associated with just one category.
###	Benefits
(Multiple choice)
Mandatory	Tick the main benefits that the end user can derive from implementing the AI component. They are reflected in 4 categories in line with the main dynamics where the major production critical issues are present: Quality, Operator Wellbeing, Machine Performance and Production Management.

It is mandatory to provide at least one benefit regardless of the category. Benefits can also be associated with just one category.
###	Use Case
(Open-ended)
Not Mandatory	Fill in by providing a brief description of the elementary scenarios and typical application use cases of the component within the production context.

The text to be inserted must be bound by a minimum and maximum number of characters. 

##	Production critical issues 
This section is intended to gather information about critical manufacturing problems for which the component provides a solution to eliminate or mitigate them. 
###	Production Critical Issues
(Multiple choice)
Not Mandatory 	Tick the main production critical issues that would be solved or mitigated by the application of the AI component. They are reflected in 4 categories in line with the main dynamics where the major production critical issues are present: Quality, Operator Wellbeing, Machine Performance and Production Management. 
Evaluate the list of the main company production criticalities, ticking the most suitable level of relevance in consideration of how much the component solves it or contributes to mitigating it. 
□	The solution can contribute mitigate the criticality
□	The solution aims to completely solve or mitigate the criticality
The categories to which the selected criticalities belong must be consistent with those of the benefits: resolving a criticality, however, can lead to benefits in different contexts.

It is mandatory to indicate at least one critical issue regardless of the section. If no critical issues are found, the user has the freedom not to select any but is obliged to indicate it by writing in field Other.

###	Worker skills
This section collects information about the skills and aspects of the workers who will be using the component. It has the purpose of understanding if skills are needed by the user in order to be able to sell the component to the most competent workers or with the necessary training material.
####	Basic Skills
(Multiple choice)	Tick the main Basic Skills necessary to use the AI component.
Process skills are procedures that contribute to the more rapid acquisition of knowledge and skill across a variety of domains: Active Learning, Critical Thinking, Learning Strategies, Monitoring.
The list provided derives from the codes of  O*NET OnLine (Browse by Basic Skills).

#### Cross-Functional Skills
(Multiple choice)	Tick the main Cross Functional Skills necessary to use the AI component. 
Cross-functional skills are developed capacities that facilitate performance of activities that occur across jobs. They are classified in 5 categories: Complex Problem-Solving Skills, Resource Management Skills, Social Skills, System Skills, Technical Skills.
The list provided derives from the codes of  O*NET OnLine (Browse by Cross-Functional Skills). 

### Support resources
This section collects information necessary for providing all the web-based resources, such as video, which could support the phases of deployment and usage of the component.
#### Support Resource
(Open-ended)
Not Mandatory	Fill in by reporting the support documents. 

The exclusive insertion of URL must be the constraint.

##	Technical component specifications
###	System requirements and specifications
This section collects information and data regarding the parameters relating to the FIWARE integration and the architecture characteristics.
#### Multiuser
(Single choice)
Mandatory	Tick the multi-user specification of the AI component:
- Yes, users share the same instance 
#### Multitenancy
(Single choice)
Mandatory	Tick the multi-tenant specification of the AI component: 
- Yes, the component supports multi tenancy so that several instances of the component can run on single machine
#### Dashboard
(Open-ended)	Fill in by reporting the component dashboard link or landing page accessible through a web browser.
#### Operating System
(Multiple choice)
Mandatory	Tick, the Operating System that support component release: Apple iOS; Apple macOS; Microsoft Windows; Google’s Android OS and Unix-like OS.
#### CPU
(Open-ended)
Mandatory	Fill in by reporting the CPU’s (Central Processing Unit) specifications required by the component. The unit of measure is in nr of Cores. 

The exclusive entry of numeric values must be the constraint.

#### GPU
(Open-ended)
Mandatory	Fill in by reporting the GPU (Graphics Processing Unit) specifications required by the AI component.

The exclusive entry of numeric values must be the constraint.

#### Disk Space
(Open-ended)
Mandatory	Fill in by reporting the amount of Disk Space required by the AI component.

The exclusive entry of numeric values must be the constraint.

#### RAM
(Open-ended)
Mandatory	Fill in by reporting the amount of memory required by the AI component.

The exclusive entry of numeric values must be the constraint.

#### UM
(Single choice)
Mandatory)	Select the most suitable unit of measure of GPU, RAM and Disk Space among those provided: KB, MB, GB.
#### Connectivity
(Open-ended)
Mandatory	Fill in by providing the type of connectivity used, specifying the name of the protocol.


###	Hardware dependencies
This section collects information necessary to provide a description of any hardware required or recommended for component operation. For example, if a component requires a specific camera to work, it should be listed here. It may also have non-mandatory hardware such as additional sensors etc. that can be used by the component.
#### Name
(Open-ended)
Not Mandatory	Fill in the Name field, by providing the name of the hardware.

The user is shown a single empty field and the possibility of adding new ones to fill out.
	Role
(Open-ended)
Not Mandatory	Fill in the Role field, by providing information about the role of the hardware and whether it provides input/output data for the component or is a sink for the information provided by the component.
	Dependency 
(Single choice)
Not Mandatory	Tick the option that indicated the dependencies level of the hardware:
- Yes, this type of HW is required for basic functionalities. 
- Yes, a specific unique HW type is required for basic functionalities.
- No, the HW reported would be used for additional functionalities.
For each HW specified in the first field, compilation of the dependency level is mandatory.

### Software dependencies
This section collects information necessary to provide a description of any software required or recommended for component operation. It may also have non-mandatory software considered as additional modules that allow to increase its value in terms, for example, of functionality.
#### Name 
(Open-ended)
Not Mandatory
	Fill in the Name field, by providing the name of the software.

The user is shown a single empty field and the possibility of adding new ones to fill out.
	Role
(Open-ended)
Not Mandatory	Fill out in the Role field, by providing information about the role of the software.
	Version
(Open-ended)
Not Mandatory	Fill in the Version field, by providing the version of the software.
	Dependencies level
(Single choice)
Not Mandatory	Tick the option that indicated the dependencies level of the software:
- Yes, this type of SW is required for basic functionalities.  
- Yes, a specific unique SW type is required for basic functionalities. 
- No, the SW reported would be used for additional functionalities.

For each SW specified in the first field, compilation of the dependency level is mandatory.
	Provide the RAMP ID
(Open-ended)
Not Mandatory	Fill in by providing the link of software datasheet.
 
The exclusive insertion of RAMP ID must be the constraint. There must be a link for selecting the IDs already present or a function for verifying the existence of the reported ID.
##	I&O Data Model
This section collects Input and Output data model information necessary for creating a visual representation of the component and for describing the communication connections between data, structures, and subsystems.
###	Input Entities
(Multiple choice)
Mandatory	Tick the type of Input NGSI Entities used by the component.  They are clustered in four macro-categories: Factory, Devices, Measurements, Workers.  

It is mandatory to indicate at least one Input Entity regardless of the section. If no Input Entity is found, the user has the freedom not to select any but is obliged to indicate it by writing in field Other.
####	Other
(Open-ended)
Not Mandatory)	Provide the name of Input entities that are absent from the proposed ones.
Provide the name of the Input Data Model that is not present among those provided.
### Output Entities
(Multiple choice)
Mandatory	Tick the type of Output NGSI Entities used by the component.  They are clustered in four macro-categories: Factory, Devices, Measurements, Workers.  

It is mandatory to indicate at least one Output Entity regardless of the section. If no Output Entity is found, the user has the freedom not to select any but is obliged to indicate it by writing in field Other.
#### Other
(Open-ended)
Not Mandatory)	Provide the name of Output entities that are absent from the proposed ones.
Provide the name of the Output Data Model that is not present among those provided.
### DataModel Link
(Open-ended)
Not Mandatory	Fill in providing the link of another Input and/or Output Data Model that are not provided in the Input Entities and Output Entities fields. 

The compilation involves the insertion of a link which may lead to the code of the Data Model, which is not known, as it is not present in the list provided above, thus in “Input Entities” and “Output Entities” fields. If at least one of the “Other” fields is filled, is mandatory to provide the link of its Data Model.

## Public Endpoints 
This section collects information necessary for describing the component in case it has interfaces that are accessible publicly.
###	OAPI
(Single choice)
Not Mandatory	Tick if any OpenAPI specification exists (Public endpoint for a managed instance enables data access to your managed instance from outside the virtual network). 
□	Yes, there are OpenAPI specifications that describe entire API including available Endpoint
### OAPIjson
(Open-ended)
Not Mandatory	Fill in by providing the Json file for the OpenAPI specification. 

The exclusive insertion of Json file must be the constraint

